# doc2md

`doc2md` — консольная утилита для преобразования документов TXT, HTML/HTM и DOCX в Markdown. В качестве входного файла можно указать локальный путь или HTTP(S)-ссылку.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/) 

## Установка

Требуется Python 3.9 или новее.

### pip

```bash
git clone <URL-репозитория>
cd MDproject
python -m venv .venv
```

Активируйте виртуальное окружение и установите зависимости проекта:

```bash
python -m pip install --upgrade pip
python -m pip install typer[all] html2text python-docx mammoth pdfplumber requests click
```

### Poetry

```bash
poetry install
poetry run python -m src.cli.app --help
```

### Docker

```bash
docker build -t doc2md .
docker run --rm doc2md --help
```

Для конвертации локальных файлов передайте рабочую папку в контейнер:

```bash
docker run --rm -v "${PWD}:/data" doc2md /data/report.docx /data/report.md
```

В PowerShell вместо `${PWD}` также можно использовать `${PWD.Path}`.

## Использование

Общий вид команды:

```bash
python -m src.cli.app INPUT OUTPUT [OPTIONS]
```

Примеры:

```bash
# Текстовый файл
python -m src.cli.app notes.txt notes.md

# HTML-файл
python -m src.cli.app page.html page.md

# DOCX-документ с созданием папки output
python -m src.cli.app report.docx output/report.md

# Документ по URL
python -m src.cli.app https://example.com/article.html article.md

# Явное указание формата, когда расширение отсутствует или неверно
python -m src.cli.app download result.md --format html

# Перезапись уже существующего результата
python -m src.cli.app report.docx report.md --force
```

## Поддерживаемые форматы

| Расширение | Входной формат | Библиотека / обработчик |
| --- | --- | --- |
| `.txt` | Обычный текст UTF-8 | `TxtParser` |
| `.html`, `.htm` | HTML | `html2text` / `HtmlParser` |
| `.docx` | Microsoft Word Open XML | `mammoth` / `DocxParser` |

В репозитории есть `PdfParser` на базе `pdfplumber`, но в текущей версии он не зарегистрирован в CLI, поэтому `.pdf` через команду `convert` пока не поддерживается.

## Опции CLI

| Аргумент или флаг | Обязателен | Описание |
| --- | --- | --- |
| `INPUT` | Да | Путь к исходному файлу либо HTTP(S)-URL. |
| `OUTPUT` | Да | Путь к создаваемому Markdown-файлу. Родительские папки создаются автоматически. |
| `--format TEXT` | Нет | Принудительно задаёт формат входа: `txt`, `html` или `docx`. Точку перед расширением можно не указывать. |
| `--force` | Нет | Разрешает перезаписать существующий выходной файл. |
| `--install-completion` | Нет | Устанавливает автодополнение для текущей оболочки. |
| `--show-completion` | Нет | Выводит скрипт автодополнения для текущей оболочки. |
| `--help` | Нет | Показывает справку Typer. |

## Ошибки

Утилита выводит сообщение в `stderr` и завершает работу с кодом `1`.

```console
$ python -m src.cli.app absent.docx output.md
Error: File not found: absent.docx
```

```console
$ python -m src.cli.app presentation.pptx output.md
Error: Unsupported file extension: .pptx
```

Если файл результата уже существует, добавьте `--force`:

```console
$ python -m src.cli.app report.docx report.md
Error: Output file already exists: report.md. Use --force to overwrite it.
```

При недопустимом явном формате будет выведен список доступных форматов:

```console
$ python -m src.cli.app report.docx report.md --format pdf
Error: Unsupported format 'pdf'. Supported formats: txt, html, htm, docx
```

## Разработка

Установите зависимости, затем запускайте проверки из корня репозитория:

```bash
# Тесты
python -m pytest

# Линтер
ruff check .

# Форматирование
black --check .

# Сборка Docker-образа
docker build -t doc2md .
```


## Автор и контакты

Автор: gZEVI

Контакты: 
mail:`sergorbachev27@gmail.com` , `gorbachev.sa.1@gmail.com` :
tg: @gZEVI
