import traceback
from bottle import Bottle, response, request, run
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
import os

from ollama_setup import CHROMA_PATH, OLLAMA_ADDRESS, OLLAMA_MODEL, OLLAMA_PORT, TOP_K

app = Bottle()

def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Origin, Authorization'

app.add_hook('after_request', enable_cors)
# Helper function to get list of PDFs
def get_pdf_list():
    pdf_path = "uploaded_pdfs"
    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)
    return [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]

def rag_pipeline(query, filename, chat_history, top_K=TOP_K):
    # Load embeddings and vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_K})
    ollama = ChatOllama(address=OLLAMA_ADDRESS, port=OLLAMA_PORT, model=OLLAMA_MODEL)
    
    # **Step 1: Combine conversation history**
    user_messages = [user_msg for user_msg, _ in chat_history]
    combined_query = " ".join(user_messages + [query])  # Combine previous user messages and current query
    
    # **Step 2: Retrieve documents using combined query**
    filter_condition = {"source": filename}
    most_relevant_docs = retriever.get_relevant_documents(combined_query, filter=filter_condition)
    
    context = "\n".join([doc.page_content for doc in most_relevant_docs[:top_K]])
    
    # Prepare the prompt messages
    messages = [
        ("system", f"You are a helpful AI assistant that can answer questions about the text using RAG with attached context: {context}"),
    ]
    # Add conversation history
    for user_msg, assistant_msg in chat_history:
        messages.append(("user", user_msg))
        messages.append(("assistant", assistant_msg))
    # Add the new user query
    messages.append(("user", query))
    
    # Invoke the model
    result = ollama.invoke(messages)
    
    # Return the assistant's reply
    return result.content

# Endpoint for chatbot
@app.route('/chat', method=['OPTIONS', 'POST'])
def chat_endpoint():
    if request.method == 'OPTIONS':
        response.content_type = 'application/json'
        return {}
    elif request.method == 'POST':
        response.content_type = 'application/json'
        try:
            data = request.json
            if not data:
                response.status = 400
                return {"error": "No data provided"}
            query = data.get("query")
            file_name = data.get("pdf")
            chat_history = data.get("history", [])
            if not query or not file_name:
                response.status = 400
                return {"error": "Missing 'query' or 'pdf' in the request body"}
            result = rag_pipeline(query, file_name, chat_history)
            return {"response": result}
        except Exception as e:
            # Log the error (optional)
            import traceback
            traceback.print_exc()
            response.status = 500
            return {"error": f"Internal server error: {str(e)}"}

# Endpoint for uploading PDF
@app.route('/upload-pdf', method=['OPTIONS', 'POST'])
def upload_pdf_endpoint():
    enable_cors()
    if request.method == 'OPTIONS':
        response.content_type = 'application/json'
        return {}
    elif request.method == 'POST':
        response.content_type = 'application/json'
        file = request.files.get("file")
        if not file:
            response.status = 400
            return {"error": "No file uploaded"}
        if not file.filename.endswith(".pdf"):
            response.status = 400
            return {"error": f"{file.filename}: Invalid file type. Please upload a PDF"}
        try:
            # Save PDF to a directory
            pdf_path = "uploaded_pdfs"
            if not os.path.exists(pdf_path):
                os.makedirs(pdf_path)
            file_path = os.path.join(pdf_path, file.filename)
            file.save(file_path)

            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            if not documents:
                response.status = 400
                return {"error": f"{file.filename}: No content extracted from the PDF"}

            # Extract text from documents
            text = " ".join([doc.page_content for doc in documents])

            if not text.strip():
                response.status = 400
                return {"error": f"{file.filename}: Empty file uploaded"}

            # Split text into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=400,
                length_function=len,
                add_start_index=True,
            )
            chunks = splitter.split_text(text)

            # Embed chunks and store in vectorstore
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
            vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
            # Create Document objects for each chunk
            documents = [
                Document(page_content=chunk, metadata={"source": file.filename})
                for chunk in chunks
            ]

            # Add Document objects to the vector store
            vectorstore.add_documents(documents)

            return {"message": f"{file.filename} uploaded and processed successfully"}
        except Exception as e:
            # Log the error traceback
            traceback.print_exc()
            response.status = 500
            return {"error": f"Error processing file: {str(e)}"}

# Endpoint for listing PDFs
@app.route('/list-pdfs', method=['GET', 'OPTIONS'])
def list_pdfs():
    enable_cors()
    if request.method == 'OPTIONS':
        response.content_type = 'application/json'
        return {}
    elif request.method == 'GET':
        response.content_type = 'application/json'
        pdf_list = get_pdf_list()
        return {"pdfs": pdf_list}

# Endpoint for deleting PDF
@app.route('/delete-pdf', method=['POST', 'OPTIONS'])
def delete_pdf():
    enable_cors()
    if request.method == 'OPTIONS':
        response.content_type = 'application/json'
        return {}
    elif request.method == 'POST':
        response.content_type = 'application/json'
        data = request.json
        if not data or 'pdf' not in data:
            response.status = 400
            return {"error": "No PDF specified for deletion"}
        pdf_name = data['pdf']
        pdf_path = os.path.join("uploaded_pdfs", pdf_name)
        if not os.path.exists(pdf_path):
            response.status = 400
            return {"error": f"PDF {pdf_name} does not exist"}
        try:
            # Delete PDF file
            os.remove(pdf_path)
            # Remove associated data from vectorstore
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
            vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
            vectorstore.delete_texts(filter={"source": pdf_name})
            return {"message": f"{pdf_name} deleted successfully"}
        except Exception as e:
            response.status = 500
            return {"error": f"Error deleting PDF: {str(e)}"}

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True, reloader=True)