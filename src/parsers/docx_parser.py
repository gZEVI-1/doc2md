"""DOCX parser based on mammoth."""

from pathlib import Path

import mammoth

from ..exceptions import DocxParseError
from .base import BaseParser


class DocxParser(BaseParser):
    """Convert ``.docx`` documents into Markdown with mammoth."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def parse(self, source: Path | str) -> str:
        path = Path(source)
        if not path.is_file():
            raise FileNotFoundError(f"DOCX file not found: {path}")

        try:
            with path.open("rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
        except (OSError, ValueError, KeyError) as error:
            raise DocxParseError(f"Failed to parse DOCX file '{path}': {error}") from error

        self.messages = [message.message for message in result.messages]
        return result.value

    def supported_extensions(self) -> list[str]:
        return [".docx"]
