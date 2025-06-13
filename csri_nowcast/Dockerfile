ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# 1) System-Bibliotheken & -Header
RUN apk update && apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base       \   # gcc, g++, make, musl-dev, libc-dev
    linux-headers    \
    eccodes          \   # ecCodes-Runtime
    eccodes-dev      \   # ecCodes-Header für pygrib
    libffi-dev       \   # für cffi
    jpeg-dev         \   # für Pillow (falls benötigt)
    git

# 2) Python-Kommando „python“ verlinken & pip absichern
RUN ln -sf /usr/bin/python3 /usr/bin/python \
 && python3 -m ensurepip \
 && pip3 install --upgrade pip setuptools wheel

# 3) Python-Abhängigkeiten via pip
RUN pip3 install --no-cache-dir \
    numpy \
    requests \
    pygrib

# 4) Add-on-Skripte kopieren und ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# 5) Startkommando
CMD [ "/run.sh" ]
