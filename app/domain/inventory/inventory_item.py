from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.inventory.value_objects import MovementType, Quantity
from app.domain.shared.value_objects import SKU


@dataclass
class InventoryItem:
    sku: SKU
    quantity: Quantity
    id: UUID = field(default_factory=uuid4)

    def apply(self, quantity: Quantity, movement_type: MovementType) -> None:
        if movement_type == MovementType.IN:
            self.quantity = self.quantity + quantity
        elif movement_type == MovementType.OUT:
            self.quantity = self.quantity - quantity
        elif movement_type == MovementType.ADJUSTMENT:
            self.quantity = quantity
