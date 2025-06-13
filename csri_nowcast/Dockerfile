# ───────────────────────────────────────────────
# Stage 1: Build pygrib-Wheel mit Debian
# ───────────────────────────────────────────────
FROM python:3.9-slim AS builder

# Installieren der nativen Abhängigkeiten
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      libeccodes-dev \
      libffi-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Aus dem Builder heraus das Wheel bauen
RUN pip install --upgrade pip setuptools wheel \
 && pip wheel --wheel-dir=/wheels \
      pygrib numpy requests

# ───────────────────────────────────────────────
# Stage 2: Finales HASS-Add-on auf Alpine-Basis
# ───────────────────────────────────────────────
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Nur Python und pip nachinstallieren
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip

# Fertige Wheels übernehmen und installieren
COPY --from=builder /wheels /wheels
RUN pip3 install --no-cache-dir /wheels/*.whl

# Add-on Skripte kopieren und Start-Script ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# Start des Add-ons
CMD ["/run.sh"]
