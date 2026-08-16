"""URL download helpers."""

import requests
from pathlib import Path
from urllib.parse import unquote, urlparse

def download_file(url: str, dest_dir: Path = Path(".")) -> Path:
    """Скачивает файл по URL и сохраняет в dest_dir. Возвращает путь к файлу."""
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    # Определяем имя файла из URL или из Content-Disposition
    filename_from_url = Path(unquote(urlparse(url).path)).name
    filename = Path(filename_from_url or "download")
    if not filename.suffix:
        # Если нет расширения, пробуем взять из заголовка
        content_type = resp.headers.get('content-type', '')
        if 'html' in content_type:
            filename = filename.with_suffix('.html')
        else:
            filename = filename.with_suffix('.bin')  # fallback
    dest_path = dest_dir / filename
    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return dest_path
