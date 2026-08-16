"""Base parser abstraction."""

from abc import ABC, abstractmethod
from pathlib import Path

class BaseParser(ABC):
    """Абстрактный парсер документов."""

    @abstractmethod
    def parse(self, source: Path | str) -> str:
        """Извлекает текст (или Markdown) из источника и возвращает строку."""
        pass

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Возвращает список расширений, которые обрабатывает парсер (например, ['.html', '.htm'])."""
        pass