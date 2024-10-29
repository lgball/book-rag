from flask import Flask, jsonify, request
import fitz

app = Flask(__name__)

def pdf_to_text():
    doc = fitz.open(request.files[0])
    text = ""
    for page in doc:
        text+=page.get_text()
    
    return text

if __name__ == '__main__':
    app.run(debug=True)