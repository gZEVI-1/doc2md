"""Typer CLI application."""

import typer
from pathlib import Path
from src.parsers import ParserFactory

app = typer.Typer(help="Convert documents to Markdown")

@app.command()
def convert(
    input: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to input file or URL"),
    output: Path = typer.Argument(..., help="Path to output .md file"),
    # позже добавим опции --format, --overwrite и т.д.
):
    """Конвертирует один файл в Markdown."""
    try:
        parser = ParserFactory.get_parser(input)
        content = parser.parse(input)
        output.write_text(content, encoding='utf-8')
        typer.echo(f"✅ Converted {input} -> {output}")
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise typer.Exit(1)

if __name__ == "__main__":
    app()