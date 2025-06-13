#!/usr/bin/env python3
import pygrib
import json
import os

OUTPUT_FILE = "/share/csri_forecast.json"
GRIB_PATH = "/share/icon-d2_sample.grib2"  # Beispielpfad – passe an!

def extract_forecast_data(grib_path):
    if not os.path.exists(grib_path):
        raise FileNotFoundError(f"GRIB-Datei nicht gefunden: {grib_path}")

    grbs = pygrib.open(grib_path)
    forecasts = []

    for grb in grbs:
        if "Surface solar radiation downwards" in grb.name:
            dt = grb.validDate.isoformat()
            lat, lon = grb.latlons()
            values = grb.values

            mean_radiation = values.mean()

            risk_index = max(0, min(1, 1 - mean_radiation / 800))  # Simplifizierter CSRI

            forecasts.append({
                "timestamp": dt,
                "csri": round(risk_index, 3),
                "mean_radiation": round(mean_radiation, 1)
            })

    grbs.close()
    return forecasts

def save_forecast(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[CSRI] Forecast gespeichert in: {output_path}")

if __name__ == "__main__":
    try:
        print("[CSRI] Verarbeite GRIB-Datei...")
        forecast = extract_forecast_data(GRIB_PATH)
        save_forecast(forecast, OUTPUT_FILE)
        print("[CSRI] Fertig.")
    except Exception as e:
        print(f"[CSRI] Fehler: {e}")
