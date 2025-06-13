#!/usr/bin/with-contenv bashio

echo "[CSRI] Nowcast gestartet..."

# Beispiel-Koordinaten und GRIB-Datei
LAT=50.5
LON=8.3
GRIB="/share/icon_d2_latest.grib2"
OUT="/share/csri_nowcast.json"

python3 /csri_predict.py \
  --lat $LAT --lon $LON \
  --grib $GRIB \
  --delta 20 \
  --out $OUT

echo "[CSRI] Forecast geschrieben nach $OUT"
