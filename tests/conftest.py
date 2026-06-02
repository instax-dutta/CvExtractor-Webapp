"""Shared pytest fixtures for the CV extractor test suite."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from app import create_app  # noqa: E402


@pytest.fixture()
def app(tmp_path: Path):
    application = create_app()
    application.config["UPLOAD_FOLDER"] = str(tmp_path)
    application.config["TESTING"] = True
    application.config["WTF_CSRF_ENABLED"] = False
    return application


@pytest.fixture()
def client(app):
    return app.test_client()
