"""HTTP routes for the CV extractor application."""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

from flask import Blueprint, render_template, request, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.config import Config
from app.extractor import extract_data
from app.models import CvData
from app.workbook import build_workbook

logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)


def _allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in Config.ALLOWED_EXTENSIONS


@main_bp.route("/")
def index() -> str:
    return render_template("index.html")


@main_bp.route("/extract", methods=["POST"])
def extract():
    files: list[FileStorage] = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        return render_template("index.html", error="No files uploaded"), 400

    results: list[CvData] = []

    for file in files:
        filename = file.filename
        if not filename or not _allowed_file(filename):
            logger.warning("Skipping unsupported file: %s", filename)
            continue

        safe_name = secure_filename(filename)
        temp_dir = Path(tempfile.mkdtemp())
        file_path = temp_dir / safe_name

        try:
            file.save(str(file_path))
            data = extract_data(file_path)
            results.append(data)
            logger.info("Extracted data from %s: %s", filename, data)
        except OSError as exc:
            logger.error("File error for %s: %s", filename, exc)
        finally:
            try:
                file_path.unlink(missing_ok=True)
                temp_dir.rmdir()
            except OSError:
                pass

    if not results:
        return render_template("index.html", error="No valid data extracted"), 400

    workbook = build_workbook(results)
    output_path = Path(tempfile.gettempdir()) / Config.OUTPUT_FILENAME
    workbook.save(str(output_path))

    return send_file(
        str(output_path),
        as_attachment=True,
        download_name=Config.OUTPUT_FILENAME,
    )
