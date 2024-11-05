from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import os
import shutil
from tqdm import tqdm

CHROMA_PATH = "data\\chroma"
DATA_PATH = "data\\test"
TESTING = True


def main():
    my_documents = load_documents()
    my_chunks = chunk_documents(my_documents)
    store_chunks(my_chunks)

def load_documents():
    if TESTING:
        print("Loading the documents:")
        loader = DirectoryLoader(DATA_PATH, glob="*.txt", show_progress=True)
    else:
        loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents

def chunk_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=400,
        length_function=len,
        add_start_index=True,
    )
    
    if TESTING:
        print("Chunking the documents:", end=' ')
        chunks = text_splitter.split_documents(documents)
        print("Done.")

    else:
        chunks = text_splitter.split_documents(documents)

    return chunks


def store_chunks(chunks):
    # Checking if the database already exists and deleting it if it does.
    if os.path.exists(CHROMA_PATH):
        if TESTING:
            answer = input("Database already exists. Enter (y or yes) to delete existing database. Anything else will cause the script to exit:\n")
            
            if answer.lower == "yes" or answer.lower() == "y":
                shutil.rmtree(CHROMA_PATH)
            else:
                print("Keeping preexisting database. Exiting function.")
                return 
        else:
            shutil.rmtree(CHROMA_PATH)

        
    # Setting up the embeddings
    if TESTING:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", show_progress=True)
    else:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    if TESTING:
        print("Storing the chunks of text in a vector database:")
    # Creating a Chroma database from the chunked text.
    vectordb = Chroma.from_documents(
        chunks, 
        collection_metadata={"hnsw:space": "cosine"},
        embedding=embeddings, 
        persist_directory=CHROMA_PATH,
    )


main()
