from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.inventory.value_objects import MovementType, Quantity
from app.domain.shared.value_objects import SKU


@dataclass
class MovementLine:
    sku: SKU
    quantity: Quantity


@dataclass
class StockMovement:
    type: MovementType
    lines: list[MovementLine]
    id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.lines:
            raise ValueError("A movement must have at least one line")
