# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm AS builder

# Outils de build minimaux pour les extensions C/Fortran (numpy, scipy, structuralcodes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    gfortran \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installer uv (résolveur Rust ultra-rapide)
RUN pip install --no-cache-dir uv

# Copier les fichiers de dépendances d'abord (cache Docker optimisé)
COPY pyproject.toml README.md ./
COPY src/ src/

# Installer avec uv (ignore les extras "dev" et "eurocode")
RUN uv pip install --system --no-cache-dir -e .

# Image finale — plus légère
FROM python:3.12-slim-bookworm

# Librairies runtime minimales si besoin plus tard
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libopenblas0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "eurocode_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
