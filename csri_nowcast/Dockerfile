FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

# Optional: Basis-Tools zum Debuggen installieren
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Beispiel: run.sh und csri_predict.py reinlegen (werden noch nicht genutzt)
COPY run.sh /run.sh
COPY csri_predict.py /csri_predict.py
RUN chmod +x /run.sh

# Du kannst später in der Shell selbst Python nachinstallieren
CMD ["bash"]

