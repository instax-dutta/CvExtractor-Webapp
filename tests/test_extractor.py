"""Unit tests for the CV extractor utility module."""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.extractor import (
    _extract_email,
    _extract_name,
    _extract_phone,
    _extract_text_from_docx,
    _extract_text_from_pdf,
    extract_data,
)
from app.models import CvData


class TestExtractName:
    def test_basic_two_word_name(self) -> None:
        assert _extract_name("John Doe") == "John Doe"

    def test_three_word_name(self) -> None:
        assert _extract_name("John Michael Doe") == "John Michael Doe"

    def test_hyphenated_name(self) -> None:
        assert _extract_name("Jean-Pierre Dupont") == "Jean-Pierre Dupont"

    def test_no_title_case_sequence(self) -> None:
        assert _extract_name("hello world foo bar") == ""

    def test_empty_string(self) -> None:
        assert _extract_name("") == ""

    def test_name_with_apostrophe(self) -> None:
        assert _extract_name("Patrick O'Brien") == "Patrick O'Brien"

    def test_single_name_only(self) -> None:
        assert _extract_name("John") == ""


class TestExtractEmail:
    def test_basic_email(self) -> None:
        assert _extract_email("Contact: john@example.com") == "john@example.com"

    def test_no_email(self) -> None:
        assert _extract_email("no email here") == ""

    def test_subaddress(self) -> None:
        assert _extract_email("john+tag@example.co.uk") == "john+tag@example.co.uk"


class TestExtractPhone:
    def test_dash_separated(self) -> None:
        assert _extract_phone("Call 555-123-4567") == "555-123-4567"

    def test_dot_separated(self) -> None:
        assert _extract_phone("555.123.4567") == "555.123.4567"

    def test_international_format(self) -> None:
        assert _extract_phone("+1 (555) 123-4567") == "+1 (555) 123-4567"

    def test_uk_format(self) -> None:
        assert _extract_phone("+44 20 7946 0958") == "+44 20 7946 0958"

    def test_with_extension(self) -> None:
        assert _extract_phone("555-123-4567 ext. 42") == "555-123-4567 ext. 42"

    def test_no_phone(self) -> None:
        assert _extract_phone("no number here") == ""

    def test_parenthesized_area_code(self) -> None:
        assert _extract_phone("(555) 123-4567") == "(555) 123-4567"


class TestExtractTextFromPdf:
    def test_returns_joined_text(self) -> None:
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1"
        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2"

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page1, mock_page2]

        with patch("app.extractor.PdfReader", return_value=mock_reader):
            result = _extract_text_from_pdf(io.BytesIO(b"pdf-bytes"))

        assert result == "Page 1\nPage 2"

    def test_empty_pages_handled(self) -> None:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = None

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        with patch("app.extractor.PdfReader", return_value=mock_reader):
            result = _extract_text_from_pdf(io.BytesIO(b"pdf-bytes"))

        assert result == ""


class TestExtractTextFromDocx:
    def test_returns_paragraph_text(self, tmp_path: Path) -> None:
        docx_path = tmp_path / "sample.docx"
        docx_path.write_bytes(b"PK\x05\x06" + b"\x00" * 18)

        from unittest.mock import MagicMock, patch
        mock_doc = MagicMock()
        mock_doc.paragraphs = [MagicMock(text="Hello"), MagicMock(text="World")]

        with patch("app.extractor.docx.Document", return_value=mock_doc):
            result = _extract_text_from_docx(docx_path)

        assert result == "Hello\nWorld"


class TestExtractData:
    def test_pdf_extraction(self, tmp_path: Path) -> None:
        pdf_path = tmp_path / "cv.pdf"

        with patch("app.extractor.PdfReader") as mock_pdf_reader:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = (
                "Alice Smith\nalice@example.com\n+1 (555) 111-2222"
            )
            mock_pdf_reader.return_value.pages = [mock_page]
            pdf_path.write_bytes(b"%PDF-1.4")

            result = extract_data(pdf_path)

        assert result.name == "Alice Smith"
        assert result.email == "alice@example.com"
        assert result.phone == "+1 (555) 111-2222"

    def test_unsupported_extension(self, tmp_path: Path) -> None:
        txt_path = tmp_path / "cv.txt"
        txt_path.write_text("hello")
        result = extract_data(txt_path)
        assert isinstance(result, CvData)
        assert result.name == ""
        assert result.email == ""
        assert result.phone == ""

    def test_missing_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "ghost.pdf"
        result = extract_data(missing)
        assert isinstance(result, CvData)
