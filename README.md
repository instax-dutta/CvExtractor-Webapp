# CV Extractor

CV Extractor is a web application that allows you to extract crucial information from a collection of resumes or CVs in various file formats (PDF, DOCX). The application can identify and extract email addresses, contact numbers, and the overall text content from the uploaded files, and compile the extracted data into a structured Excel file for easy viewing and analysis.

## Features

- Upload multiple CV files simultaneously
- Extract email addresses, phone numbers, and text content from PDF and DOCX files
- Generate an Excel file containing the extracted data
- Download the generated Excel file for further processing

## Getting Started

These instructions will help you set up the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

```
git clone https://github.com/username/cv-extractor.git
```

2. Navigate to the project directory:

```
cd cv-extractor
```

3. Create and activate a virtual environment (optional but recommended):

```
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

4. Install the required Python packages:

```
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask development server:

```
python app.py
```

2. Open your web browser and visit `http://localhost:5000` to access the CV Extractor application.

### Usage

1. Click the "Choose Files" button and select one or more CV files (PDF or DOCX format) from your local machine.
2. Click the "Extract" button to initiate the extraction process.
3. Once the extraction is complete, you will be prompted to download the generated Excel file containing the extracted data.

## Deployment

To deploy the application to a production server, follow these steps:

1. Install the required packages on the server:

```
pip install -r requirements.txt
```

2. Configure a web server (e.g., Nginx, Apache) to serve the Flask application.
3. Set up a reverse proxy to forward requests to the Flask application.
4. Configure the systemd service or any other process manager to run the Flask application in the background.

Refer to the [Flask Deployment Documentation](https://flask.palletsprojects.com/en/2.2.x/deploying/) for more detailed instructions on deploying Flask applications.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [python-docx](https://python-docx.readthedocs.io/en/latest/) - Python library for reading DOCX files
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) - Python library for reading PDF files
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/) - Python library for working with Excel files
