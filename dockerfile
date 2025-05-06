FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install pdm && pdm install --no-editable

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["pdm", "run", "start"]