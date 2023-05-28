from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class StadGentSensor(CoordinatorEntity, SensorEntity):
    """Stad Gent Sensor Class"""

    def __init__(self, coordinator, unique_id, name, icon):
        """Initialize the entity"""
        super().__init__(coordinator)
        self._unique_id = unique_id
        if icon is not None:
            self._attr_icon = icon
        self._attr_name = name

    @property
    def unique_id(self) -> str:
        return self._unique_id


class StadGentParkingSensor(StadGentSensor):
    """Stad Gent Parking Class"""

    def __init__(self, coordinator, parking):
        """Initialize the entity"""
        name = parking["name"]
        super().__init__(
            coordinator,
            f"stadgent_parking_{name}",
            f"Parking {name}",
            "mdi:parking",
        )
        self.__state = parking

    @property
    def _state(self):
        return self.__state

    @property
    def native_value(self):
        if self._state["temporaryclosed"] == 1:
            return 100
        return float(self._state["occupation"])

    @property
    def native_unit_of_measurement(self):
        return "%"

    @property
    def suggested_display_precision(self) -> float:
        return 0

    @property
    def suggested_unit_of_measurement(self) -> float:
        return "%"

    @property
    def state_attributes(self):
        if self._state:
            return {
                "capacity_total": self._state["totalcapacity"],
                "capacity_available": self._state["availablecapacity"],
                "capacity_left": self._state["totalcapacity"]
                - self._state["availablecapacity"],
            }
        return None
