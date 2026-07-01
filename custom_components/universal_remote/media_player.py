"""Universal Remote media_player entity.

Per the brief: "A single media player entity MAY be used to display
the current source and status, however, all state management and
source-switching logic MUST be handled by the custom integration."

So this entity is a thin display/control surface only -- select_source()
just calls the controller. It holds no state of its own.
"""
from __future__ import annotations

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerDeviceClass,
)
from homeassistant.const import STATE_OFF, STATE_ON, STATE_IDLE, STATE_PLAYING
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the universal remote media_player entity."""
    controller = hass.data[DOMAIN]["controller"]
    async_add_entities([UniversalRemoteMediaPlayer(controller)])


class UniversalRemoteMediaPlayer(MediaPlayerEntity):
    """A single entity that reflects the controller's current source/status."""

    _attr_name = "Universal Remote"
    _attr_unique_id = "universal_remote_media_player"
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_should_poll = False
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.SELECT_SOURCE
        | MediaPlayerEntityFeature.VOLUME_STEP
    )

    def __init__(self, controller) -> None:
        self._controller = controller
        controller.add_listener(self._handle_controller_update)

    def _handle_controller_update(self) -> None:
        self.schedule_update_ha_state()

    # ---------- state reflected from the controller ----------

    @property
    def state(self) -> str:
        if self._controller.tv_power != "on":
            return STATE_OFF
        if self._controller.active_source:
            return STATE_PLAYING
        return STATE_IDLE

    @property
    def source(self) -> str | None:
        return self._controller.active_source

    @property
    def source_list(self) -> list[str]:
        return self._controller.source_list

    @property
    def extra_state_attributes(self) -> dict:
        """Debug/status info -- shown on the secondary dashboard view."""
        return {
            "tv_power": self._controller.tv_power,
            "avr_power": self._controller.avr_power,
            "active_source": self._controller.active_source,
        }

    # ---------- actions: all delegate straight to the controller ----------

    async def async_turn_on(self) -> None:
        self._controller.turn_on_tv()
        self._controller.turn_on_avr()

    async def async_turn_off(self) -> None:
        self._controller.turn_off_tv()

    async def async_select_source(self, source: str) -> None:
        self._controller.select_source(source)

    async def async_volume_up(self) -> None:
        # Volume isn't part of the required state model, so this is a
        # no-op placeholder -- documented here rather than silently
        # ignored, per the "no unexplained hacks" requirement.
        pass

    async def async_volume_down(self) -> None:
        pass
