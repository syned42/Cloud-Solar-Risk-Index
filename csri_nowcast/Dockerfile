# ── STAGE 1: Baue Wheels für pygrib & Co ─────────────────────────────
FROM --platform=linux/arm64 python:3.11-slim as builder

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libeccodes-dev libjpeg-dev zlib1g-dev \
    cython3 git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Pip-Wheels bauen & Log speichern
RUN pip install --upgrade pip setuptools wheel && \
    mkdir -p /wheels && \
    pip wheel --wheel-dir=/wheels pygrib numpy requests > /wheels/build.log 2>&1 || \
    (echo "[CSRI] Fehler beim Build – siehe /wheels/build.log" && \
     cat /wheels/build.log && exit 1)

# Sicherstellen, dass pygrib gebaut wurde
RUN test -f /wheels/pygrib*.whl || \
    (echo "[CSRI] pygrib-Wheel fehlt – Build wird abgebrochen!" && exit 1)

# ── STAGE 2: Runtime Container für Home Assistant ─────────────────────
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Falls Python & pip nicht vorhanden sind, installieren
RUN apk add --no-cache python3 py3-pip || true && \
    python3 -m ensurepip || true && \
    pip3 install --upgrade pip || true

# Übernehme Wheels und installiere
COPY --from=builder /wheels /wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Dein CSRI-Code & Skript
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD ["/run.sh"]
