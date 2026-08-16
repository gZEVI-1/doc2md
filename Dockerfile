FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Копирование исходников
COPY src/ ./src/
COPY README.md .

# Точка входа
ENTRYPOINT ["python", "-m", "src.cli.app"]
# По умолчанию запускаем help
CMD ["--help"]