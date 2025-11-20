FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для данных, если её нет (хотя она будет смонтирована)
RUN mkdir -p data

CMD ["python", "main.py"]
