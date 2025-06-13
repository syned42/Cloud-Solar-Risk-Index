ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# 1) System-Pakete via apt (Debian) installieren
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-pip \
    build-essential \
    libeccodes0 \
    libeccodes-dev \
    libffi-dev \
    libjpeg-dev \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 2) pip updaten und Python-Libraries installieren
RUN python3 -m pip install --upgrade pip setuptools wheel \
 && pip3 install --no-cache-dir \
    numpy \
    requests \
    pygrib

# 3) Add-on Skripte kopieren und ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# 4) Start-Command
CMD [ "/run.sh" ]
