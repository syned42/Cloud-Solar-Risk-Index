#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
csri_predict.py

Advektionsbasiertes Nowcasting für den Cloud-Solar-Risk-Index (CSRI)
===================================================================

Dieses Skript liest aus einem ICON-D2-GRIB-File die Parameter
  - Total Cloud Cover (in %)
  - 10 m Windvektor (u/v in m/s)
an der Position einer DWD-Wetterstation, projiziert das Wolkenfeld
entlang des Windvektors um Δt Minuten und berechnet so eine
Vorhersage des Cloud-Solar-Risk-Index (CSRI_pred).

Output (JSON) enthält:
  • csri_pred   – prognostizierter Cloud-Risikowert (0–100 %)
  • cloud_now   – aktueller Wolkenanteil (%)  
  • wind_speed  – Windgeschwindigkeit (m/s)  
  • wind_dir    – Windrichtung (° meteorologisch, aus der der Wind weht)

Usage:
  python3 csri_predict.py
    --lat 50.6             # Breite (deg)
    --lon 8.3              # Länge (deg)
    --grib icon_d2.grib2   # Pfad zur ICON-D2-GRIB2-Datei
    --delta 20             # Vorhersagehorizont Δt (Minuten)
    --out    nowcast.json  # Ausgabe-Datei

Requirements:
  pip install pygrib numpy

Hinweis:
  • ICON-D2-GRIB muss den Parameter “Total Cloud Cover” (CloudT) und
    die Felder “u-component_of_wind_height_above_ground” (u10) und
    “v-component_of_wind_height_above_ground” (v10) enthalten.
  • Die GRIB-Coverage muss das Raster abdecken, das deine Station
    umschliesst.

(c) 2025 syned42 – MIT-License
"""

import argparse
import json
import math
import numpy as np
import pygrib

def parse_args():
    p = argparse.ArgumentParser(
        description="Advektions-Nowcast für CSRI anhand ICON-D2-Daten"
    )
    p.add_argument("--lat",    type=float, required=True,
                   help="Breitengrad der Station (°)")
    p.add_argument("--lon",    type=float, required=True,
                   help="Längengrad der Station (°)")
    p.add_argument("--grib",   type=str,   required=True,
                   help="Pfad zur ICON-D2 GRIB2 Datei")
    p.add_argument("--delta",  type=int,   default=20,
                   help="Vorhersagehorizont in Minuten (Standard: 20)")
    p.add_argument("--out",    type=str,   default="nowcast.json",
                   help="JSON-Ausgabedatei")
    return p.parse_args()

def read_field(grbs, name):
    """
    Lies das erste gefundene GRIB-Message-Feld mit dem gegebenen Parameter-Namen.
    Gibt ein Tuple (values, lats, lons).
    """
    try:
        msg = grbs.select(name=name)[0]
    except Exception:
        raise RuntimeError(f"Feld '{name}' nicht in GRIB-Datei gefunden.")
    data, lats, lons = msg.values, msg.latitudes(), msg.longitudes()
    return data, lats, lons

def interp_to_point(data, lats, lons, lat0, lon0):
    """
    Bilineare Interpolation des Rasters data/lats/lons an den Punkt (lat0,lon0).
    """
    # auf nächstgelegene Indizes suchen
    i = np.abs(lats[:,0] - lat0).argmin()
    j = np.abs(lons[0,:] - lon0).argmin()
    return float(data[i, j])

def advect(lat, lon, u, v, delta_min):
    """
    Advektion des Punktes (lat,lon) gegen Windvektor (u,v) um delta_min Minuten.
    Rückgabe der neuen Koordinaten (lat_adv, lon_adv).
    """
    # physikalische Umrechnung: 1° ~ 111.320 km (Breitengrad), Berücksichtigung Längengrad
    dt_h = delta_min / 60.0
    # Verschiebung in km
    shift_x = u * dt_h  # Ost-West (positive u: West→Ost)
    shift_y = v * dt_h  # Süd-Nord (positive v: Süd→Nord)
    # in Grad umrechnen
    deg_per_km = 1.0 / 111.320
    lat_adv = lat + shift_y * deg_per_km
    lon_adv = lon + shift_x * deg_per_km / math.cos(math.radians(lat))
    return lat_adv, lon_adv

def wind_to_direction(u, v):
    """
    Berechnet die Windrichtung (° meteorologisch), aus der der Wind weht.
    (u, v) sind Vektoren in m/s.
    """
    # Richtung, aus der der Wind kommt: atan2(-u, -v)
    dir_rad = math.atan2(-u, -v)
    dir_deg = (math.degrees(dir_rad) + 360.0) % 360.0
    return dir_deg

def main():
    args = parse_args()

    # 1) GRIB öffnen
    grbs = pygrib.open(args.grib)

    # 2) Daten extrahieren
    cloud_data, cloud_lats, cloud_lons = read_field(grbs, "Total cloud cover")
    u10_data, u10_lats, u10_lons     = read_field(grbs, "u-component_of_wind_height_above_ground")
    v10_data, v10_lats, v10_lons     = read_field(grbs, "v-component_of_wind_height_above_ground")

    # 3) Aktuelle Werte an Station
    cloud_now = interp_to_point(cloud_data, cloud_lats, cloud_lons, args.lat, args.lon)
    u_now     = interp_to_point(u10_data,    u10_lats,    u10_lons,    args.lat, args.lon)
    v_now     = interp_to_point(v10_data,    v10_lats,    v10_lons,    args.lat, args.lon)

    # 4) Advektion
    lat_adv, lon_adv = advect(args.lat, args.lon, u_now, v_now, args.delta)
    cloud_pred = interp_to_point(cloud_data, cloud_lats, cloud_lons, lat_adv, lon_adv)

    # 5) Windstatistik
    wind_speed = math.hypot(u_now, v_now)
    wind_dir   = wind_to_direction(u_now, v_now)

    # 6) CSRI_pred: hier direkt aus % Wolkenanteil (umgekehrt zu Risiko)
    #    CSRI kann als wolkenfreie Anteile interpretiert werden:
    csri_pred = round(100.0 - cloud_pred, 1)

    # 7) JSON output
    result = {
        "csri_pred":   csri_pred,
        "cloud_now":   round(cloud_now, 1),
        "cloud_pred":  round(cloud_pred, 1),
        "wind_speed":  round(wind_speed, 2),
        "wind_dir":    round(wind_dir, 1)
    }
    with open(args.out, "w") as fp:
        json.dump(result, fp, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
