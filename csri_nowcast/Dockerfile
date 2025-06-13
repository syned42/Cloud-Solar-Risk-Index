# ─── Stage 1: Builder auf ARM64 mit Debian ────────────────
FROM --platform=linux/arm64 python:3.11-slim as builder

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

# Systembibliotheken für pygrib + numpy
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libeccodes-dev \
    libjpeg-dev \
    zlib1g-dev \
    cython3 \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Aktuelle Piptools & Wheel bauen
RUN pip install --upgrade pip setuptools wheel && \
    pip wheel --wheel-dir=/wheels pygrib numpy requests

# ─── Stage 2: Home Assistant Add-on Runtime ───────────────
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Python & pip hinzufügen, falls noch nicht vorhanden
RUN apk add --no-cache python3 py3-pip && \
    python3 -m ensurepip && pip3 install --upgrade pip

# Wheels übernehmen und installieren
COPY --from=builder /wheels /wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Skripte übernehmen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD ["/run.sh"]
