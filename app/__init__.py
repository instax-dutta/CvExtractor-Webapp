"""CV Extractor application package."""

from __future__ import annotations

import logging

from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config import Config

csrf = CSRFProtect()


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_app() -> Flask:
    configure_logging()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=Config.SECRET_KEY,
        MAX_CONTENT_LENGTH=Config.MAX_CONTENT_LENGTH,
        UPLOAD_FOLDER=Config.UPLOAD_FOLDER,
        WTF_CSRF_TIME_LIMIT=None,
    )

    Config.ensure_upload_folder()

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    csrf.init_app(app)

    return app
