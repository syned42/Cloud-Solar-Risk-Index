# ─── Stage 1: Debian-Builder ──────────────────────────────
FROM python:3.9-slim as builder

ENV LANG C.UTF-8

# Notwendige System-Abhängigkeiten für pygrib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libeccodes-dev \
    libffi-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Python-Wheel-Verzeichnis anlegen und pygrib vorbereiten
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir=/wheels \
      pygrib numpy requests

# ─── Stage 2: HA-Add-on ───────────────────────────────────
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Python und pip im HA-Basisimage installieren
RUN apk add --no-cache python3 py3-pip && \
    python3 -m ensurepip

# Wheels aus dem Builder übernehmen
COPY --from=builder /wheels /wheels

# Installation der fertigen Python-Wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Add-on Skripte übernehmen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# Startkommando
CMD ["/run.sh"]
