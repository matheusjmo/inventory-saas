from dataclasses import dataclass
from enum import Enum


class MovementType(Enum):
    IN = "in"
    OUT = "out"
    ADJUSTMENT = "adjustment"


@dataclass(frozen=True)
class Quantity:
    value: int
    unit: str = "units"

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("Quantity cannot be negative")

    def __add__(self, other: "Quantity") -> "Quantity":
        return Quantity(self.value + other.value, self.unit)

    def __sub__(self, other: "Quantity") -> "Quantity":
        result = self.value - other.value
        if result < 0:
            raise ValueError("Resulting quantity cannot be negative")
        return Quantity(result, self.unit)
