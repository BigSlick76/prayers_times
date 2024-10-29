import logging
from .prayer_times import get_prayer_times
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    prayer_times = get_prayer_times()
    entities = [PrayerTimeSensor(prayer, time) for prayer, time in prayer_times.items()]
    async_add_entities(entities, True)

class PrayerTimeSensor(Entity):
    def __init__(self, name, state):
        self._name = name
        self._state = state

    @property
    def name(self):
        return f"Prayer Time {self._name}"

    @property
    def state(self):
        return self._state
