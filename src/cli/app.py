"""Command-line interface for converting documents to Markdown."""

from pathlib import Path
from urllib.parse import urlparse

import typer

from src.parsers.docx_parser import DocxParser
from src.parsers.html_parser import HtmlParser
from src.parsers.txt_parser import TxtParser
from src.utils.downloader import download_file

app = typer.Typer(help="Convert TXT, HTML, and DOCX documents to Markdown.")

PARSERS = (TxtParser(), HtmlParser(), DocxParser())


def is_url(value: str) -> bool:
    """Return whether *value* is an HTTP(S) URL."""
    return urlparse(value).scheme in {"http", "https"}


def get_parser(source: Path):
    """Return the parser that supports the source file extension."""
    extension = source.suffix.lower()
    for parser in PARSERS:
        if extension in parser.supported_extensions():
            return parser
    raise ValueError(f"Unsupported file extension: {extension or '(none)'}")


def get_parser_by_format(document_format: str):
    """Return the parser explicitly requested by the user."""
    normalized_format = document_format.lower().lstrip(".")
    for parser in PARSERS:
        if f".{normalized_format}" in parser.supported_extensions():
            return parser
    supported = ", ".join(extension.lstrip(".") for parser in PARSERS for extension in parser.supported_extensions())
    raise ValueError(f"Unsupported format '{document_format}'. Supported formats: {supported}")


@app.command()
def convert(
    input: str = typer.Argument(..., help="Path or HTTP(S) URL of the source document."),
    output: Path = typer.Argument(..., help="Destination Markdown file."),
    document_format: str | None = typer.Option(
        None,
        "--format",
        help="Force the input format: txt, html, or docx.",
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite an existing output file."),
) -> None:
    """Convert one document to Markdown."""
    try:
        if is_url(input):
            typer.echo(f"Downloading {input}...")
            source_path = download_file(input)
        else:
            source_path = Path(input)
            if not source_path.is_file():
                raise FileNotFoundError(f"File not found: {source_path}")

        if output.exists() and not force:
            raise FileExistsError(f"Output file already exists: {output}. Use --force to overwrite it.")

        parser = get_parser_by_format(document_format) if document_format else get_parser(source_path)
        content = parser.parse(source_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    except (OSError, ValueError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error

    typer.echo(f"Converted {source_path} -> {output}")


if __name__ == "__main__":
    app()
