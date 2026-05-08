from dataclasses import dataclass


@dataclass
class RegisterInventoryItemCommand:
    sku: str
    initial_quantity: int
    unit: str = "units"


@dataclass
class MovementLineCommand:
    sku: str
    quantity: int


@dataclass
class ApplyMovementCommand:
    movement_type: str  # "in", "out", "adjustment"
    lines: list[MovementLineCommand]
