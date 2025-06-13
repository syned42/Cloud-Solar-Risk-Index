ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Install required packages
RUN apk add --no-cache \
    py3-pip \
    py3-numpy \
    py3-requests \
    gcc \
    g++ \
    py3-setuptools \
    make \
    linux-headers \
    eccodes-dev \
    py3-pillow \
    py3-cffi \
    py3-wheel \
    py3-gribapi \
    git

# Install pygrib
RUN pip install pygrib

# Copy files
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

CMD [ "/run.sh" ]
