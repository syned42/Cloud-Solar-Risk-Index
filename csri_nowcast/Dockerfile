ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# 1) edge-Repositories hinzufügen und System-Pakete installieren
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
 && echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
 && apk update && apk add --no-cache \
    python3 \
    python3-dev \
    py3-pip \
    build-base    \   # gcc, g++, make, musl-dev, libc-dev
    eccodes       \   # ecCodes-Runtime-Bibliothek
    eccodes-dev   \   # ecCodes-Header für pygrib
    libffi-dev    \   # für cffi
    jpeg-dev      \   # für Pillow (falls nötig)
    git

# 2) pip, setuptools & wheel updaten, Python-Dependencies installieren
RUN python3 -m ensurepip \
 && pip3 install --no-cache-dir --upgrade pip setuptools wheel \
 && pip3 install --no-cache-dir \
      numpy \
      requests \
      pygrib

# 3) Add-on-Skripte kopieren & ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# 4) Startkommando
CMD ["/run.sh"]
