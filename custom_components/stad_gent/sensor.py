"""StadGent sensor."""
from .classes import (
    StadGentParkingSensor,
)
from .stadgent_api import StadGentAPI
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol

from datetime import timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
)
from .const import *
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Optional("refresh_interval", default=3 * 60): cv.Number}
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async def async_update_data():
        """Fetch data"""
        api = StadGentAPI()
        data = {"parkings": await hass.async_add_executor_job(api.getParkings)}

        return data

    # interval = config[CONF_RSS_SIGNS][CONF_RSS_SIGNS_REFRESH_INTERVAL]

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="StadGent",
        update_method=async_update_data,
        update_interval=timedelta(seconds=60 * 5),
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    entities_to_add = []

    for parking in coordinator.data["parkings"]:
        entities_to_add.append(StadGentParkingSensor(coordinator, parking["fields"]))

    async_add_entities(entities_to_add)
