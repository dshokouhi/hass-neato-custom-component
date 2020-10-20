"""Support for Neato botvac connected vacuum cleaners."""
import asyncio
from datetime import timedelta
import logging

from pybotvac import Account, Neato, Vorwerk
from pybotvac.exceptions import NeatoRobotException
import voluptuous as vol

from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_entry_oauth2_flow, config_validation as cv
from homeassistant.util import Throttle

from . import api, config_flow
from .const import (
    CONF_VENDOR,
    NEATO_CONFIG,
    NEATO_DOMAIN,
    NEATO_LOGIN,
    NEATO_MAP_DATA,
    NEATO_PERSISTENT_MAPS,
    NEATO_ROBOTS,
    VALID_VENDORS,
    VENDOR_NEATO,
    VENDOR_VORWERK,
)

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema(
    {
        NEATO_DOMAIN: vol.Schema(
            {
                vol.Required(CONF_CLIENT_ID): cv.string,
                vol.Required(CONF_CLIENT_SECRET): cv.string,
                vol.Optional(CONF_VENDOR, default=VENDOR_NEATO): vol.In(VALID_VENDORS),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ["camera", "vacuum", "switch", "sensor"]


async def async_setup(hass, config):
    """Set up the Neato component."""
    hass.data[NEATO_DOMAIN] = {}

    if NEATO_DOMAIN not in config:
        return True

    hass.data[NEATO_CONFIG] = config[NEATO_DOMAIN]

    if config[NEATO_DOMAIN][CONF_VENDOR] == VENDOR_VORWERK:
        vendor = Vorwerk()
    else:
        vendor = Neato()

    config_flow.OAuth2FlowHandler.async_register_implementation(
        hass,
        api.NeatoImplementation(
            hass,
            NEATO_DOMAIN,
            config[NEATO_DOMAIN][CONF_CLIENT_ID],
            config[NEATO_DOMAIN][CONF_CLIENT_SECRET],
            vendor.auth_endpoint,
            vendor.token_endpoint,
        ),
    )

    return True


async def async_setup_entry(hass, entry):
    """Set up config entry."""
    implementation = (
        await config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        )
    )

    session = config_entry_oauth2_flow.OAuth2Session(hass, entry, implementation)

    neatoSession = api.ConfigEntryAuth(hass, entry, session)
    hass.data[NEATO_DOMAIN][entry.entry_id] = neatoSession
    hub = NeatoHub(hass, Account(neatoSession))

    try:
        await hass.async_add_executor_job(hub.update_robots)
    except NeatoRobotException as ex:
        _LOGGER.debug("Failed to connect to Neato API")
        raise ConfigEntryNotReady from ex

    hass.data[NEATO_LOGIN] = hub

    for component in ("camera", "vacuum", "switch", "sensor"):
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass, entry):
    """Unload config entry."""
    unload_ok = all(
        await asyncio.gather(
            hass.config_entries.async_forward_entry_unload(entry, "camera"),
            hass.config_entries.async_forward_entry_unload(entry, "vacuum"),
            hass.config_entries.async_forward_entry_unload(entry, "switch"),
            hass.config_entries.async_forward_entry_unload(entry, "sensor"),
        )
    )
    if unload_ok:
        hass.data[NEATO_DOMAIN].pop(entry.entry_id)

    return unload_ok


class NeatoHub:
    """A My Neato hub wrapper class."""

    def __init__(self, hass, neato: Account):
        """Initialize the Neato hub."""
        self._hass = hass
        self.my_neato = neato

    @Throttle(timedelta(minutes=1))
    def update_robots(self):
        """Update the robot states."""
        _LOGGER.debug("Running HUB.update_robots %s", self._hass.data.get(NEATO_ROBOTS))
        self._hass.data[NEATO_ROBOTS] = self.my_neato.robots
        self._hass.data[NEATO_PERSISTENT_MAPS] = self.my_neato.persistent_maps
        self._hass.data[NEATO_MAP_DATA] = self.my_neato.maps

    def download_map(self, url):
        """Download a new map image."""
        map_image_data = self.my_neato.get_map_image(url)
        return map_image_data
