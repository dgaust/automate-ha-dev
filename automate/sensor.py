"""Support for Automate Roller Blind Batteries."""
from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    UNIT_PERCENTAGE,
    DEVICE_CLASS_SIGNAL_STRENGTH,
)
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .base import AutomateBase
from .const import AUTOMATE_HUB_UPDATE, DOMAIN
from .helpers import async_add_automate_entities


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Automate Rollers from a config entry."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    current_battery = set()
    current_signal = set()

    @callback
    def async_add_automate_sensors():
        async_add_automate_entities(
            hass, AutomateBattery, config_entry, current_battery, async_add_entities
        )
        async_add_automate_entities(
            hass, AutomateSignal, config_entry, current_signal, async_add_entities
        )

    hub.cleanup_callbacks.append(
        async_dispatcher_connect(
            hass,
            AUTOMATE_HUB_UPDATE.format(config_entry.entry_id),
            async_add_automate_sensors,
        )
    )


class AutomateBattery(AutomateBase):
    """Representation of a Automate cover battery sensor."""

    device_class = DEVICE_CLASS_BATTERY
    unit_of_measurement = UNIT_PERCENTAGE
    device_state_attributes = {"somerandostate": 12445}

    @property
    def name(self):
        """Return the name of roller."""
        return f"{super().name} Battery"

    @property
    def state(self):
        """Return the state of the device battery."""
        return self.roller.battery_percent

    # @property
    # def unique_id(self):
    #     """Return a unique identifier for this device."""
    #     return f"{self.roller.id}-battery"

    # @property
    # def device_info(self):
    #     """XXX Return the device info."""
    #     info = super().device_info
    #     info["via_device"] = (DOMAIN, self.roller.id)
    #     return info


class AutomateSignal(AutomateBase):
    """Representation of a Automate cover WiFi signal sensor."""

    device_class = DEVICE_CLASS_SIGNAL_STRENGTH
    unit_of_measurement = "dB"

    @property
    def name(self):
        """Return the name of roller."""
        print("XXX Wifi Name:", "{super().name} WiFi Signal")
        return f"{super().name} WiFi Signal"

    @property
    def state(self):
        """Return the state of the device signal strength."""
        return self.roller.signal

    @property
    def unique_id(self):
        """Return a unique identifier for this device."""
        return f"{self.roller.id}-signal"

    @property
    def device_info(self):
        """XXX Return the device info."""
        info = super().device_info
        info["via_device"] = (DOMAIN, self.roller.id)
        print()
        print("XXX returing: ", info)
        return info