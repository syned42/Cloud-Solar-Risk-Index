import asyncio
import json
import logging
from datetime import timedelta

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_GRIB    = "grib_path"
CONF_STATION= "station_id"
CONF_DELTA  = "forecast_minutes"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LATITUDE): cv.latitude,
    vol.Required(CONF_LONGITUDE): cv.longitude,
    vol.Required(CONF_GRIB): cv.string,
    vol.Optional(CONF_DELTA, default=20): cv.positive_int,
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    lat  = config[CONF_LATITUDE]
    lon  = config[CONF_LONGITUDE]
    grib = config[CONF_GRIB]
    delta= config[CONF_DELTA]

    async_add_entities([CSRINowcastSensor(lat, lon, grib, delta)], True)

class CSRINowcastSensor(Entity):
    def __init__(self, lat, lon, grib, delta):
        self._lat      = lat
        self._lon      = lon
        self._grib     = grib
        self._delta    = delta
        self._state    = None
        self._attrs    = {}

    @property
    def name(self):
        return "CSRI Nowcast"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs

    @property
    def unit_of_measurement(self):
        return "%"

    async def async_update(self):
        """Ruft csri_predict.py auf und parst das JSON-Resultat."""
        cmd = [
            hass.config.config_dir + "/custom_components/csri_nowcast/csri_predict.py",
            "--lat", str(self._lat),
            "--lon", str(self._lon),
            "--grib", self._grib,
            "--delta", str(self._delta),
            "--out", "/tmp/csri_nowcast.json"
        ]
        proc = await asyncio.create_subprocess_exec(*cmd)
        await proc.wait()
        # JSON einlesen
        try:
            with open("/tmp/csri_nowcast.json") as fp:
                data = json.load(fp)
            self._state = data["csri_pred"]
            self._attrs  = {
                "cloud_now":  data["cloud_now"],
                "cloud_pred": data["cloud_pred"],
                "wind_speed": data["wind_speed"],
                "wind_dir":   data["wind_dir"]
            }
        except Exception as e:
            _LOGGER.error("Fehler beim Parsen der Nowcast-Daten: %s", e)
