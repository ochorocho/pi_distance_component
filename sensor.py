"""Platform for Pi Pico and HC-SR04 sensor integration."""
from __future__ import annotations

import logging

import requests
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    PLATFORM_SCHEMA
)
from homeassistant.const import CONF_NAME, CONF_URL, LENGTH_CENTIMETERS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

# Validate configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_URL): cv.url,
    vol.Required(CONF_NAME): cv.string,
})

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
        hass: HomeAssistant,
        config: ConfigType,
        async_add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    entity_name = config.get(CONF_NAME)
    url = config[CONF_URL]
    async_add_entities([PicoDistanceSensor(entity_name, url, SensorDeviceClass)])


class PicoDistanceSensor(SensorEntity):
    """Representation of a Pico Distance Sensor."""

    def __init__(self, name: str, url: str, device_class, unit: str = LENGTH_CENTIMETERS) -> None:
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._url = url
        self._available = False

    @property
    def available(self):
        """Return if sensor is available."""

        return self._available

    def update(self) -> None:
        """Fetch data - this is the only method to fetch data for Home Assistant"""

        try:
            response = requests.get(self._url, timeout=5)
            self._available = True
        except:
            self._available = False
            _LOGGER.info("No response from " + self._url)
            return

        result = response.json()
        self._attr_native_value = result["distance"]
