import requests
import json

# Define the URL and payload
url = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "mistral:latest",
    "prompt": "Why is the sky blue?"
}

# Send the POST request
response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, stream=True)

# Initialize an empty string to collect the response parts
full_response = ""

# Iterate over the streamed response
for line in response.iter_lines():
    if line:
        part = json.loads(line.decode('utf-8'))
        full_response += part["response"]
        if part.get("done"):
            break

print("Full Response:", full_response)
