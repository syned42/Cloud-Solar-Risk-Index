ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Edge-Repos für ecCodes aktivieren und System-Bibliotheken installieren
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
      python3 \
      python3-dev \
      py3-pip \
      build-base \
      linux-headers \
      eccodes \
      eccodes-dev \
      libffi-dev \
      git

# pip updaten und Python-Module installieren
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir \
      numpy \
      requests \
      pygrib

# Add-on-Skripte kopieren und ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD ["/run.sh"]
