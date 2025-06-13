ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# System-Pakte installieren (gcc, ecCodes etc.)
RUN apk update && apk add --no-cache \
    python3 \
    py3-pip \
    build-base        \
    linux-headers     \
    eccodes-dev       \
    jpeg-dev          \
    libffi-dev        \
    git

# Python-Dependencies installieren
RUN pip3 install --no-cache-dir \
    pygrib \
    numpy \
    requests

# Add-on-Skripte kopieren
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
