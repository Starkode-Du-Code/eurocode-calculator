# syntax=docker/dockerfile:1
FROM --platform=linux/amd64 python:3.12-slim-bookworm AS builder

# Outils COMPLETS pour compiler triangle + autres libs C/Fortran
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    gfortran \
    libblas-dev \
    liblapack-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier les fichiers de dépendances d'abord (cache Docker optimisé)
COPY pyproject.toml README.md ./
COPY src/ src/

# Installer les dépendances avec pip (et non uv) car `triangle` — dépendance d'eurocodepy —
# n'a pas de wheel précompilée pour toutes les plateformes (ex: Linux ARM64 sur Snap Deploy).
# pip compile alors triangle depuis les sources grâce aux outils de build installés ci-dessus.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

# Image finale — plus légère
FROM --platform=linux/amd64 python:3.12-slim-bookworm

# Librairies runtime minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libblas3 \
    liblapack3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier depuis le builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/src /app/src
COPY --from=builder /app/pyproject.toml /app/pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "eurocode_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
