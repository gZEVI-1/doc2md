"""Plain-text parser."""

from pathlib import Path
from .base import BaseParser

class TxtParser(BaseParser):
    def parse(self, source: Path | str) -> str:
        path = Path(source)
        return path.read_text(encoding='utf-8')

    def supported_extensions(self) -> list[str]:
        return ['.txt']