"""Data models for CV extraction."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CvData:
    name: str = ""
    email: str = ""
    phone: str = ""
