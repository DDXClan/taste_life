# Используем базовый образ Python
FROM python:3.9

ENV database_url='login:password@host:port/database'
# Устанавливаем зависимости
COPY ../requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . /app

