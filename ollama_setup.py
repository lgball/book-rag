

import subprocess
import atexit
import signal
import os
import time
import requests
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama.chat_models import ChatOllama

# Define paths to store data
CHROMA_PATH = "src/data/chroma"
DATA_PATH = "src/data/test"
# Ollama server configuration
OLLAMA_ADDRESS = "localhost"
OLLAMA_PORT = 11434
OLLAMA_LOG_PATH = "logs/ollama.log"
OLLAMA_MODEL = "llama3.2:3b"
TOP_K = 5

# Store subprocesses to clean up later
subprocesses = []

def setup_chroma():
    # Checking if the Chroma directory exists
    if not os.path.exists(CHROMA_PATH):
        print(f"Creating Chroma directory at {CHROMA_PATH}")
        os.makedirs(CHROMA_PATH)
    else:
        print(f"Chroma directory already exists at {CHROMA_PATH}")

def initialize_chroma():
    print("Initializing Chroma with HuggingFaceEmbeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return vectorstore

def start_ollama_server():
    # Check if the Ollama server is not running by sending a GET request to the base address and port
    try:
        response = requests.get(f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}")
        if response.status_code == 200:
            print("Ollama server already running.")
            return
    except requests.ConnectionError:
        print("Ollama server is not running. Starting Ollama server...")

    # Start Ollama server
    with open(OLLAMA_LOG_PATH, 'a') as log:
        proc = subprocess.Popen(["ollama", "serve"], stdout=log, stderr=log)
        subprocesses.append(proc)
    
    # Now check if the server is running
    for _ in range(5):
        time.sleep(5)
        try:
            response = requests.get(f"http://{OLLAMA_ADDRESS}:{OLLAMA_PORT}")
            if response.status_code == 200:
                print("Ollama server started successfully.")
                return
        except requests.ConnectionError:
            print("Ollama server not started yet. Retrying in 5 seconds...")
    print("Ollama server failed to start. Please check the logs for more information.")

def start_services():
    setup_chroma()
    initialize_chroma()
    start_ollama_server()


def cleanup_subprocesses():
    if not subprocesses:
        print("No subprocesses to clean up.")
        return
    for proc in subprocesses:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

# Register cleanup function to be called on exit
atexit.register(cleanup_subprocesses)

# Handle signals for graceful shutdown
def signal_handler(sig, frame):
    cleanup_subprocesses()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Start other backend services
def initial_setup():
    start_services()


    # Retrieve the most relevant text chunks

def main():
    print("Starting backend services...")
    initial_setup()
    print("Backend services started.")
    try:
        print("Press Ctrl+C to stop services")
        running = True
        while running:
            signal.pause()
    except KeyboardInterrupt:
        print("Shutting down services...")

if __name__ == "__main__":
    main()