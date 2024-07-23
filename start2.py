import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import requests
import json
import logging
import os
from contextlib import contextmanager

# Configuration parameters
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
OLLAMA_API_URL = "http://127.0.0.1:11434/api"
COLLECTION_NAME = "LEEDS_DATA_SCIENCE_MEETUP"
VECTOR_SIZE = 4096
EMBEDDING_MODEL = "mistral:latest"
SAMPLE_DATA_FILE = 'exampledata.txt'

# Configure logging
log_file = 'script.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger()

def log_divider():
    divider = "\n" + "-"*50 + "\n"*2 + "-"*50 + "\n"*2 + "-"*50
    logger.info(divider)

@contextmanager
def log_section(section_name):
    log_divider()
    logger.info(f"STARTING {section_name}")
    log_divider()
    try:
        yield
    except Exception as e:
        logger.error(f"ERROR in {section_name}: {e}")
        log_divider()
        raise
    logger.info(f"COMPLETED {section_name}")
    log_divider()

# Initialize the Qdrant client
with log_section("INITIALIZING QDRANT CLIENT"):
    qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Function to get embeddings from Ollama API
def get_embedding(text):
    url = f"{OLLAMA_API_URL}/embed"
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text
    }
    
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get embeddings: {e}")
        raise
    
    embeddings = response_data.get('embeddings', [])
    if not embeddings:
        raise ValueError("No embeddings found in the response.")
    
    embedding = embeddings[0]
    if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
        raise ValueError("Embedding must be a list of floats.")
    
    return embedding

# Function to get completion from Ollama API
def get_completion(prompt):
    url = f"{OLLAMA_API_URL}/generate"
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": prompt
    }
    
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, stream=True)
        response.raise_for_status()
        full_response = ""
        for line in response.iter_lines():
            if line:
                part = json.loads(line.decode('utf-8'))
                full_response += part["response"]
                if part.get("done"):
                    break
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to get completion: {e}")
        raise
    
    return full_response

# Check if the collection exists
with log_section("CHECKING COLLECTION"):
    if qdrant_client.collection_exists(COLLECTION_NAME):
        logger.info("COLLECTION ALREADY EXISTS. SKIPPING UPSERT.")
    else:
        logger.info("CREATING NEW COLLECTION")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )

# Read sample data and upsert points into Qdrant
with log_section("READING SAMPLE DATA"):
    if not os.path.exists(SAMPLE_DATA_FILE):
        logger.error(f"Sample data file {SAMPLE_DATA_FILE} does not exist.")
        raise FileNotFoundError(f"Sample data file {SAMPLE_DATA_FILE} does not exist.")
    
    with open(SAMPLE_DATA_FILE, 'r') as file:
        data = file.read()

    sample_data = data.split('\n\n')  # Split by double newline for paragraphs

with log_section("GENERATING AND UPSERTING EMBEDDINGS"):
    points = []
    for i, text in enumerate(sample_data):
        text = text.strip()
        if not text:
            continue
        embedding = get_embedding(text)
        point = PointStruct(
            id=i,
            vector=embedding,
            payload={"id": i, "text": text}
        )
        points.append(point)

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    for point in points:
        logger.info(f"Inserted point ID: {point.id}, Text: {point.payload['text']}")

# Define a query text and search Qdrant
query_text = "What are the command line parameters for creating an MSIX package MsixPackagingTool.exe create-package ?"

with log_section("GENERATING QUERY EMBEDDING"):
    query_embedding = get_embedding(query_text)

logger.info(f"Query embedding: {query_embedding}")

with log_section("SEARCHING QDRANT"):
    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=9,  # Number of results to return
        with_payload=True
    )

    relevant_texts = [result.payload['text'] for result in search_result]

logger.info(f"Number of relevant vectors found: {len(search_result)}")
for result in search_result:
    logger.info(f"Search result - Score: {result.score}, Text: {result.payload['text']}")

# Construct the system prompt and completion prompt
system_prompt = "You want to use the MSIX packaging with a template. no small talk ."
context = " ".join(relevant_texts)
completion_prompt = f"{system_prompt}\n\nBased on the context provided from the vector database, here is the relevant information:\n\n{context}\n\n"

logger.info(f"Completion prompt: {completion_prompt}")

# Print the completion (formatting the response directly from the retrieved vectors)
logger.info("Answer")
logger.info(completion_prompt)
print("Formatted Completion:", completion_prompt)
