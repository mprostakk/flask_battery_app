import enum


class ChargeStateEnum(enum.Enum):
    charging = "charging"
    discharging = "discharging"
    maintenance = "maintenance"

    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
