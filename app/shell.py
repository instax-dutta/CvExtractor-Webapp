"""Optional Flask shell context configuration."""

from __future__ import annotations

from app import create_app
from app.extractor import extract_data
from app.models import CvData
from app.workbook import build_workbook

app = create_app()


@app.shell_context_processor
def make_shell_context() -> dict:
    return {
        "app": app,
        "CvData": CvData,
        "extract_data": extract_data,
        "build_workbook": build_workbook,
    }
