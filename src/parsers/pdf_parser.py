"""PDF parser."""

import pdfplumber
from pathlib import Path
from .base import BaseParser

class PdfParser(BaseParser):
    def parse(self, source: Path | str) -> str:
        text = ""
        with pdfplumber.open(source) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        return text.strip()

    def supported_extensions(self) -> list[str]:
        return ['.pdf']