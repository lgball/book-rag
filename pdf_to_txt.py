from bottle import Bottle, response, request, run
import fitz
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ollama_setup import CHROMA_PATH, OLLAMA_ADDRESS, OLLAMA_MODEL, OLLAMA_PORT, TOP_K

app = Bottle()

def enable_cors():
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Origin, Authorization'
def rag_pipeline(query, filename, top_K=TOP_K):
    enable_cors()

    response.content_type = 'application/json'
    # Load Chroma vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    # Load Ollama model
    ollama = ChatOllama(model=OLLAMA_MODEL, address=OLLAMA_ADDRESS, port=OLLAMA_PORT)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_K})
    
    # Retrieve only chunks related to the given filename
    most_relevant_text = retriever.invoke(query, filter={"source": filename})
    
    prompt_message = [
        ("system", f"You are a helpful AI assistant that can answer questions about the text using RAG with attached context {most_relevant_text}."),
        ("user", query)
    ]
    result = ollama.invoke(prompt_message)
    return result


@app.route('/chatbot', method='OPTIONS')
@app.post('/chatbot')
def get_response():
    enable_cors()
    response.content_type = 'application/json'
    query = request.json
    if query is None:
        response.status = 400
        return {"error": "No query provided"}, 400
    file_name = query.get("pdf_text")
    user_prompt = query.get("user_prompt")
    result = rag_pipeline(query, file_name)
    return {"response": result}




@app.route('/upload-pdf', method='OPTIONS')
def handle_options():
    enable_cors()
    response.content_type = 'application/json'
    return {}

@app.post('/upload-pdf')
def pdf_to_text():
    enable_cors()


    response.content_type = 'application/json'

    file = request.files.get("file")

    if 'file' not in request.files:
        response.status = 400
        return {"error": "No file part"}, 400

    if file.filename == '':
        response.status = 400
        return {"error": "No selected file"}, 400
    
    if file.filename.endswith(".pdf") != True:
        print("i am the wrong type")
        response.status = 400
        print(f"Received file: {file.filename}, type: {type(file)}")
        return {"error": file.filename + ": Incompatible file type. Please upload a PDF!"}, 400

    print(type(file))
    # if no cors issue, 

    try:
    
        doc = fitz.open(stream=file.file, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        if text == "":
            return {"error": file.filename + ": Empty file uploaded. Please upload a different file!"}, 400
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=400,
            length_function=len,
            add_start_index=True,
        )
        chunks = splitter.split_text(text)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        chunked_embeddings = embeddings.embed_documents(chunks)

        vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        vectorstore.add_texts(texts=chunks, metadatas=[{"source": file.filename}] * len(chunks),embeddings=chunked_embeddings)
        return {"text": text}
    except:
        # if theres a cors issue, handle the raw byte encoding conversion

        file.file.seek(0)
        file_data = file.file.read()

        doc = fitz.open(stream=file_data, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()
        
        if text == "":
            return {"error": file.filename + ": Empty file uploaded. Please upload a different file!"}, 400

        return {"text": text}
    
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, reloader=True)