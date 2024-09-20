# Embeddings and Vector-Based Search with Qdrant and Ollama API

## Author: Ryan Mangan
## Date: 2024-07-23

This repository contains two scripts demonstrating how to use embeddings for vector-based search and processing responses using the Qdrant and Ollama APIs.

## Prerequisites

- Python 3.7+
- Docker

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/embeddings-vector-search.git
cd embeddings-vector-search
```

### 2. Install the Required Packages

```bash
pip install numpy qdrant-client requests logging
```

### 3. Set Up Qdrant Using Docker

1. Pull the Qdrant Docker image:
    ```bash
    docker pull qdrant/qdrant
    ```

2. Run the Qdrant container:
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```

### 4. Set Up Ollama API

Refer to the [Ollama API GitHub repository](https://github.com/ollama/ollama) for instructions on setting up and running the Ollama API.

**Note**: You can also use other models such as Azure Open AI or other open-source models for generating embeddings and processing responses.

### 5. Prepare Sample Data

Place your sample data in a file named `exampledata.txt` in the same directory as the scripts. The data should be formatted with paragraphs separated by double newlines (`\n\n`).

## Script 1: Vector-Based Search with Qdrant (`start2.py`)

### Summary:
This script demonstrates how to use embeddings for vector-based search with Qdrant and the Ollama API. It initializes a Qdrant client, checks for or creates a collection, generates embeddings for sample data, upserts them into the Qdrant database, and performs a search query to retrieve relevant data based on embeddings.

### Configuration Parameters:
- `QDRANT_HOST`: Host for the Qdrant service.
- `QDRANT_PORT`: Port for the Qdrant service.
- `OLLAMA_API_URL`: URL for the Ollama API.
- `COLLECTION_NAME`: Name of the collection in Qdrant.
- `VECTOR_SIZE`: Size of the vectors used in the embeddings.
- `EMBEDDING_MODEL`: Model used for generating embeddings.
- `SAMPLE_DATA_FILE`: File containing the sample data to be processed.

### Run the Script:

```bash
python start2.py
```

### Logging:
The script logs its activities to a file named `script.log` and also outputs logs to the console for real-time monitoring.

## Script 2: Using LLM Completions to Process Responses (`start3.py`)

### Summary:
This script demonstrates how to use embeddings for processing responses using the Ollama API without database features. It initializes a Qdrant client, checks for or creates a collection, generates embeddings for sample data, upserts them into the Qdrant database, and performs a search query to retrieve relevant data based on embeddings. Finally, it constructs a completion prompt using the retrieved data and fetches a formatted response from the Ollama API using LLM completions.

### Configuration Parameters:
- `QDRANT_HOST`: Host for the Qdrant service.
- `QDRANT_PORT`: Port for the Qdrant service.
- `OLLAMA_API_URL`: URL for the Ollama API.
- `COLLECTION_NAME`: Name of the collection in Qdrant.
- `VECTOR_SIZE`: Size of the vectors used in the embeddings.
- `EMBEDDING_MODEL`: Model used for generating embeddings.
- `SAMPLE_DATA_FILE`: File containing the sample data to be processed.

### Run the Script:

```bash
python start3.py
```

### Logging:
The script logs its activities to a file named `script.log` and also outputs logs to the console for real-time monitoring.

## Sample Data:
The sample data should be placed in a file named `exampledata.txt` in the same directory as the scripts. The data should be formatted with paragraphs separated by double newlines (`\n\n`).

## License:
This project is licensed under the MIT License.

⚠️ Disclaimer
Use at Your Own Risk
The scripts and content provided in this repository are for demonstration and educational purposes only. By using the scripts in this repository, you agree that:

No Warranty:

These scripts are provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.
No Liability:

In no event shall the authors, maintainers, or anyone else associated with this repository be held liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the scripts or the use or other dealings in the scripts.
Test Before Use:

These scripts are intended for demonstration and testing purposes. Before using them in production environments, test thoroughly in a safe environment to avoid unintended consequences.
User Responsibility:

The user assumes all responsibility for determining the appropriateness of using the scripts for their specific situation and for protecting their systems and data from any risks.
No Official Support:

These scripts do not come with official support. Any issues encountered are the user's responsibility to resolve. Community support may be available, but there are no guarantees.
Changes and Modifications:

The scripts may be updated or modified over time, and no guarantee is made that future changes will maintain backward compatibility or intended behavior.
By using this repository, you agree to the above terms.

