"""Run the CV extractor development server.

Usage:
    python run.py
"""

from __future__ import annotations

import logging

from dotenv import load_dotenv

from app import create_app
from app.config import Config

logger = logging.getLogger(__name__)


def main() -> None:
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    Config.ensure_upload_folder()
    logger.info("Starting CV Extractor on http://127.0.0.1:5000")

    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
