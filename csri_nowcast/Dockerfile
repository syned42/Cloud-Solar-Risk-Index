ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# 1) System-Dependencies (Compiler, ecCodes, Header)
RUN apk update && apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base \
    linux-headers \
    eccodes \
    eccodes-dev \
    libffi-dev \
    jpeg-dev \
    git

# 2) Python-Setup und pip-Upgrade
RUN ln -sf /usr/bin/python3 /usr/bin/python \
 && python3 -m ensurepip \
 && pip3 install --upgrade pip setuptools wheel

# 3) Python-Bibliotheken installieren
RUN pip3 install --no-cache-dir \
    numpy \
    requests \
    pygrib

# 4) Add-on-Skripte kopieren und ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# 5) Start-Befehl
CMD ["/run.sh"]
