from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "data\\chroma"

# Setting up the embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vectordb = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings, collection_metadata={"hnsw:space": "cosine"})

my_query = input("Placeholder for testing until we integrate this with the website. Enter query here: ")

most_relevant_text = vectordb.similarity_search_with_relevance_scores(my_query, k=2)

print(most_relevant_text)