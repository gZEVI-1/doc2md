
from pathlib import Path
from .base import BaseParser
from .txt_parser import TxtParser
from .html_parser import HtmlParser

class ParserFactory:
    _parsers = [TxtParser(), HtmlParser()]  # позже добавим DOCX, PDF

    @classmethod
    def get_parser(cls, source: Path | str) -> BaseParser:
        path = Path(source)
        ext = ''.join(path.suffixes)   # поддерживаем .tar.gz? но для простоты берём последний
        # Упрощённо: берём последнее расширение
        ext = path.suffix.lower()
        for parser in cls._parsers:
            if ext in parser.supported_extensions():
                return parser
        raise ValueError(f"Unsupported file extension: {ext}")