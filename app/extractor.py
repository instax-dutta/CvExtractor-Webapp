"""CV text extraction and data parsing utilities."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import IO

import docx
from pypdf import PdfReader

from app.models import CvData

logger = logging.getLogger(__name__)

_NAME_RE = re.compile(
    r"\b(?:[A-Z][a-z]*(?:['\u2019-][A-Z][a-z]+)?\s+){1,}[A-Z][a-z]*(?:['\u2019-][A-Z][a-z]+)?\b"
)
_EMAIL_RE = re.compile(r"[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(
    r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{3,4}"
    r"(?:\s?(?:ext|x(?:t(?:ension)?)?)[.:]?\s?\d{1,5})?"
)


def _extract_text_from_pdf(file: IO[bytes]) -> str:
    pdf_reader = PdfReader(file)
    return "\n".join(
        page.extract_text() or "" for page in pdf_reader.pages
    )


def _extract_text_from_docx(file_path: Path) -> str:
    doc = docx.Document(str(file_path))
    return "\n".join(para.text for para in doc.paragraphs)


def _extract_name(text: str) -> str:
    match = _NAME_RE.search(text)
    return match.group() if match else ""


def _extract_email(text: str) -> str:
    match = _EMAIL_RE.search(text)
    return match.group() if match else ""


def _extract_phone(text: str) -> str:
    match = _PHONE_RE.search(text)
    return match.group() if match else ""


def extract_data(file_path: Path) -> CvData:
    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            with open(file_path, "rb") as f:
                text = _extract_text_from_pdf(f)
        elif suffix == ".docx":
            text = _extract_text_from_docx(file_path)
        else:
            logger.warning("Unsupported file type: %s", suffix)
            return CvData()
    except (FileNotFoundError, PermissionError) as exc:
        logger.error("Failed to read %s: %s", file_path, exc)
        return CvData()

    if not text.strip():
        logger.warning("No text extracted from %s", file_path)
        return CvData()

    return CvData(
        name=_extract_name(text),
        email=_extract_email(text),
        phone=_extract_phone(text),
    )
