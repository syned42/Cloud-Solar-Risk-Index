ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Edge-Repos aktivieren & System-Bibliotheken installieren
RUN echo "https://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories && \
    echo "https://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
      python3 \
      python3-dev \
      py3-pip \
      build-base \
      grib_api        \
      grib_api-dev    \
      libffi-dev      \
      git

# pip updaten & Python-Abhängigkeiten installieren
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir \
      numpy \
      requests \
      pygrib

# Skripte kopieren & ausführbar machen
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD ["/run.sh"]
