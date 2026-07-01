"""TV and AVR power switches.

These entities are deliberately "dumb" -- they don't hold any state
of their own. They read from and call into the shared RemoteController.
That's what makes this maintainable: if the power-on logic changes,
you edit controller.py once, not two separate switch classes.
"""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity, SwitchDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DOMAIN, STATE_ON


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the TV and AVR power switches."""
    controller = hass.data[DOMAIN]["controller"]

    async_add_entities(
        [
            TvPowerSwitch(controller),
            AvrPowerSwitch(controller),
        ]
    )


class _BasePowerSwitch(SwitchEntity):
    """Shared plumbing for both power switches."""

    _attr_device_class = SwitchDeviceClass.SWITCH
    _attr_should_poll = False

    def __init__(self, controller) -> None:
        self._controller = controller
        controller.add_listener(self._handle_controller_update)

    def _handle_controller_update(self) -> None:
        """Called by the controller whenever state changes anywhere."""
        self.schedule_update_ha_state()


class TvPowerSwitch(_BasePowerSwitch):
    """Represents the mock TV's power state."""

    _attr_name = "TV Power"
    _attr_unique_id = "universal_remote_tv_power"
    _attr_icon = "mdi:television"

    @property
    def is_on(self) -> bool:
        return self._controller.tv_power == STATE_ON

    async def async_turn_on(self, **kwargs) -> None:
        self._controller.turn_on_tv()

    async def async_turn_off(self, **kwargs) -> None:
        self._controller.turn_off_tv()


class AvrPowerSwitch(_BasePowerSwitch):
    """Represents the mock AVR's power state."""

    _attr_name = "AVR Power"
    _attr_unique_id = "universal_remote_avr_power"
    _attr_icon = "mdi:audio-video"

    @property
    def is_on(self) -> bool:
        return self._controller.avr_power == STATE_ON

    async def async_turn_on(self, **kwargs) -> None:
        self._controller.turn_on_avr()

    async def async_turn_off(self, **kwargs) -> None:
        self._controller.turn_off_avr()
