from flask import Flask, render_template, request, flash, redirect

import openai

import fitz  # PyMuPDF
import os

app = Flask(__name__)
  # Change this to a secure random key
app.config['SECRET_KEY'] = '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'
openai.api_key = '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'
  # Replace with your OpenAI API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    # Save the uploaded file to a temporary location
    temp_path = 'temp.pdf'
    pdf_file.save(temp_path)

    # Perform text extraction using PyMuPDF
    extracted_text = extract_text_from_pdf(temp_path)

    # Remove the temporary file
    os.remove(temp_path)

    return render_template('result.html', text=extracted_text)

def extract_text_from_pdf(pdf_path):
    # Text extraction using PyMuPDF
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += page.get_text()

    return text

if __name__ == '__main__':
    app.run(debug=True)
