"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
import secrets
from pathlib import Path


class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    MAX_CONTENT_LENGTH: int = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    UPLOAD_FOLDER: str = os.environ.get("UPLOAD_FOLDER", "uploads")
    ALLOWED_EXTENSIONS: frozenset = frozenset({".pdf", ".docx"})
    OUTPUT_FILENAME: str = "output.xlsx"

    @classmethod
    def ensure_upload_folder(cls) -> None:
        Path(cls.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
