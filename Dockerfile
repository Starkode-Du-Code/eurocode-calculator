FROM python:3.12-slim-bookworm

# Installer les outils de build si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "eurocode_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]