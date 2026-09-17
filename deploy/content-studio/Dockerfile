FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MEMORY_PALACE_ENV=production \
    MEMORY_PALACE_HOST=0.0.0.0 \
    MEMORY_PALACE_PORT=8000 \
    MEMORY_PALACE_ADMIN_ENABLED=false \
    MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false \
    MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false \
    MEMORY_PALACE_GITHUB_ALLOW_MERGE=false

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
RUN mkdir -p /app/server_data && chown -R app:app /app/server_data

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3).read()" || exit 1

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
