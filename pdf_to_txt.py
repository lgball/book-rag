from flask import Flask, jsonify, request
from flask_cors import CORS
import fitz

app = Flask(__name__)
CORS(app)

@app.route('/upload-pdf', methods=['GET','POST'])

def pdf_to_text():
    
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        if file.name == '':
            return jsonify({"error": "No selected file"}), 400

        if file.filename.endswith(".pdf") != True:
            return jsonify({"error": file.filename + ": Incompatible file type. Please upload a PDF!"}), 400


        doc = fitz.open(stream=file.read(), filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text()

        if text == "":
            return jsonify({"error": file.filename + ": Empty file uploaded. Please upload a different file!"}), 400

        return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)