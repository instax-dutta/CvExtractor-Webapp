# CV Extractor

[![CI](https://github.com/instax-dutta/CvExtractor-Webapp/actions/workflows/ci.yml/badge.svg)](https://github.com/instax-dutta/CvExtractor-Webapp/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)

Upload PDF and DOCX resumes, extract name/email/phone from each, and download a structured Excel workbook.

## Features

- **Batch upload** — select multiple files at once via drag-and-drop or file picker
- **PDF & DOCX support** — extracts text from both formats
- **Smart extraction** — regex-based parsing for names, email addresses, and phone numbers (international formats supported)
- **Excel export** — results compiled into a single `.xlsx` workbook
- **Dark mode** — respects system `prefers-color-scheme`
- **Accessible** — keyboard-navigable, ARIA labels, `prefers-reduced-motion` support
- **CSRF-protected** — form submissions secured with Flask-WTF

## Tech Stack

| Layer      | Technology                                |
|------------|-------------------------------------------|
| Backend    | Flask 3.x + Gunicorn                      |
| PDF        | pypdf                                     |
| DOCX       | python-docx                               |
| Excel      | openpyxl                                  |
| Security   | Flask-WTF (CSRF protection)               |
| Frontend   | Vanilla HTML/CSS/JS (no framework)        |
| CI/CD      | GitHub Actions (ruff + pytest + Docker)   |

## Prerequisites

- Python 3.10+
- pip

## Quick Start

### Local Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open http://localhost:5000.

### Docker

```bash
docker compose up
```

Open http://localhost:8000.

## Configuration

Environment variables (`.env` file):

| Variable             | Default       | Description                   |
|----------------------|---------------|-------------------------------|
| `SECRET_KEY`         | auto-generated| Flask session signing key     |
| `MAX_CONTENT_LENGTH` | `16777216`    | Max upload size (bytes)       |
| `UPLOAD_FOLDER`      | `uploads`     | Directory for uploaded files  |

`SECRET_KEY` is auto-generated via `secrets.token_hex(32)` if not set.

## Project Structure

```
├── app/
│   ├── __init__.py        # App factory, CSRF init
│   ├── config.py          # Env-based configuration
│   ├── extractor.py       # Text extraction + regex parsing
│   ├── models.py          # CvData dataclass
│   ├── routes.py          # GET / and POST /extract
│   ├── shell.py           # Flask shell helpers
│   ├── workbook.py        # Excel workbook builder
│   ├── static/
│   │   ├── css/main.css   # Full-featured stylesheet
│   │   └── js/main.js     # Drag-drop, validation, spinner
│   └── templates/
│       └── index.html     # Upload form
├── tests/
│   ├── conftest.py        # pytest fixtures
│   ├── test_extractor.py  # Extraction logic tests
│   └── test_routes.py     # Route tests
├── run.py                 # Dev server entry point
├── wsgi.py                # Production entry point
├── pyproject.toml         # Build config + ruff + pytest
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Single-service compose
└── .github/workflows/ci.yml
```

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Linting

```bash
pip install ruff
ruff check .
```

Uses ruff with rulesets: E, F, W, I, N, UP, B, SIM.

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

Runs ruff lint + format on commit.

## API

### `POST /extract`

Upload one or more CV files.

- **Content-Type:** `multipart/form-data`
- **Field name:** `files[]`
- **Accepted formats:** `.pdf`, `.docx`
- **Response:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (Excel download)

Returns `400` with error message on empty upload or extraction failure.

## Deployment

```bash
docker build -t cv-extractor .
docker run -p 8000:8000 cv-extractor
```

The Docker image uses gunicorn with a multi-stage build for a slim production image.

## License

MIT
