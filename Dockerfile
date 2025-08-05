FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Спочатку requirements.txt
COPY requirements.txt .

# Ставимо залежності
RUN pip install --upgrade pip && pip install -r requirements.txt

# Потім копіюємо сам код
COPY ./theatre_project /app
