# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Copier les fichiers de dépendances d'abord (cache Docker optimisé)
COPY pyproject.toml README.md ./
COPY src/ src/

# Installer les dépendances core (eurocodepy inclus, structuralcodes EXCLU —
# voir extra [capacity] si capacity-based design est nécessaire)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# Image finale — plus légère
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copier depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "eurocode_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
