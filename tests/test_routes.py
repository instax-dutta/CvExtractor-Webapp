"""HTTP route tests for the CV extractor application."""

from __future__ import annotations

from pathlib import Path

from app.config import Config


class TestConfig:
    def test_defaults(self) -> None:
        assert frozenset({".pdf", ".docx"}) == Config.ALLOWED_EXTENSIONS
        assert Config.OUTPUT_FILENAME == "output.xlsx"
        assert Config.MAX_CONTENT_LENGTH == 16 * 1024 * 1024
        assert Config.SECRET_KEY is not None

    def test_ensure_upload_folder_creates(self, tmp_path: Path) -> None:
        target = tmp_path / "uploads"
        Config.UPLOAD_FOLDER = str(target)
        Config.ensure_upload_folder()
        assert target.is_dir()


class TestRoutes:
    def test_index_returns_200(self, client) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        assert b"CV Extractor" in resp.data

    def test_extract_no_files_returns_400(self, client) -> None:
        resp = client.post("/extract")
        assert resp.status_code == 400
