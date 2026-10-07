FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY hala_api ./hala_api
COPY data ./data

RUN pip install --no-cache-dir -e .

RUN useradd -m -u 1000 hala && chown -R hala:hala /app
USER hala

EXPOSE 8000

CMD ["uvicorn", "hala_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
