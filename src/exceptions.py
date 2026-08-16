"""Project-specific exceptions."""


class DocumentConversionError(Exception):
    """Base exception for document conversion failures."""


class DocxParseError(DocumentConversionError):
    """Raised when a DOCX document cannot be converted to Markdown."""
