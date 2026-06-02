"""Excel workbook builder for extracted CV data."""

from __future__ import annotations

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from app.models import CvData


def build_workbook(results: list[CvData]) -> openpyxl.Workbook:
    workbook = openpyxl.Workbook()
    worksheet: Worksheet | None = workbook.active
    if worksheet is None:
        worksheet = workbook.create_sheet("CV Data")
    else:
        worksheet.title = "CV Data"
    worksheet.append(["Name", "Email", "Phone"])
    for data in results:
        worksheet.append([data.name, data.email, data.phone])
    return workbook
