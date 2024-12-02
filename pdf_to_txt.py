from bottle import Bottle, response, request, run
import fitz
import mysql.connector

app = Bottle()

def enable_cors():
    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Origin, Authorization'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@Corinthians129"
)

@app.route('/api/data', method='GET')
def get_data():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM your_table")
    results = cursor.fetchall()
    cursor.close()

    # Set response headers for JSON
    response.content_type = 'application/json'
    return {"data": results}

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