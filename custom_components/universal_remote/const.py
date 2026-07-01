"""Constants for the Universal Remote (mock) integration.

Keeping all shared config in one place means adding a 5th source later
is a one-line change here, not a hunt through media_player.py.
"""

DOMAIN = "universal_remote"

# The 4 required sources. Add/remove entries here only -- nothing else
# in the integration needs to change to support a different source list.
SOURCES = [
    "Apple TV",
    "Source 2",
    "Source 3",
    "Source 4",
]

# Icons per source, used purely for dashboard polish.
SOURCE_ICONS = {
    "Apple TV": "mdi:apple",
    "Source 2": "mdi:gamepad-variant",
    "Source 3": "mdi:youtube-tv",
    "Source 4": "mdi:disc-player",
}

STATE_ON = "on"
STATE_OFF = "off"

ATTR_TV_POWER = "tv_power"
ATTR_AVR_POWER = "avr_power"
ATTR_ACTIVE_SOURCE = "active_source"
ATTR_SOURCE_LIST = "source_list"
