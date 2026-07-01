"""Universal Remote (mock) integration.

Sets up ONE shared RemoteController instance and stores it in
hass.data so every platform (switch, media_player) can grab the
same instance -- this is what guarantees a single source of truth
instead of each entity inventing its own state.
"""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.discovery import async_load_platform
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .controller import RemoteController

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "media_player"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the universal_remote integration from configuration.yaml."""
    hass.data.setdefault(DOMAIN, {})

    controller = RemoteController()
    hass.data[DOMAIN]["controller"] = controller

    _LOGGER.info("Universal Remote (mock) controller initialized")

    # Forward to platforms so switch.py / media_player.py can pick up
    # the same controller instance and build their entities from it.
    for platform in PLATFORMS:
        hass.async_create_task(
            async_load_platform(hass, platform, DOMAIN, {}, config)
        )

    return True
