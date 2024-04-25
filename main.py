from flask import Flask, render_template, request, send_file
import os
import docx
import PyPDF2
import openpyxl
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    files = request.files.getlist('files')
    if not files:
        return render_template('index.html', error='No files uploaded'), 400

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'CV Data'
    worksheet.append(['Name', 'Email', 'Phone'])

    for file in files:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        name, email, phone = extract_data(file_path)
        worksheet.append([name, email, phone])

        os.remove(file_path)

    output_path = os.path.join(app.root_path, 'output.xlsx')
    workbook.save(output_path)

    return send_file('output.xlsx', as_attachment=True)

def extract_data(file_path):
    text = ''
    name = ''
    email = ''
    phone = ''

    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()

    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + '\n'

    # Extract name
    name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
    name_match = re.search(name_pattern, text)
    if name_match:
        name = name_match.group()

    # Extract email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email:
        email = email.group()

    # Extract phone number
    phone = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
    if phone:
        phone = phone.group()

    return name, email, phone

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(port=5000, debug=True)