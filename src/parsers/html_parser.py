"""HTML parser."""

import html2text
from pathlib import Path
from .base import BaseParser

class HtmlParser(BaseParser):
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.body_width = 0   # отключаем перенос строк

    def parse(self, source: Path | str) -> str:
        path = Path(source)
        html = path.read_text(encoding='utf-8')
        return self.converter.handle(html)

    def supported_extensions(self) -> list[str]:
        return ['.html', '.htm']