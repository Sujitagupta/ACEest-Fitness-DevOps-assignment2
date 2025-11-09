FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ARG APP_VERSION=v1.0
ENV APP_VERSION=${APP_VERSION}
EXPOSE 5000
CMD ["gunicorn", "app.main:create_app()", "-b", "0.0.0.0:5000", "--workers", "2"]
