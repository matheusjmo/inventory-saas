from uuid import UUID

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.repository import InventoryRepository, StockMovementRepository
from app.domain.inventory.stock_movement import StockMovement
from app.domain.shared.value_objects import SKU


class InMemoryInventoryRepository(InventoryRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, InventoryItem] = {}

    async def get_by_sku(self, sku: SKU) -> InventoryItem | None:
        return next((i for i in self._store.values() if i.sku == sku), None)

    async def get_by_id(self, id: UUID) -> InventoryItem | None:
        return self._store.get(id)

    async def save(self, item: InventoryItem) -> None:
        self._store[item.id] = item

    async def list_all(self) -> list[InventoryItem]:
        return list(self._store.values())


class InMemoryStockMovementRepository(StockMovementRepository):
    def __init__(self) -> None:
        self._store: list[StockMovement] = []

    async def save(self, movement: StockMovement) -> None:
        self._store.append(movement)

    async def list_by_sku(self, sku: SKU) -> list[StockMovement]:
        return [
            m for m in self._store
            if any(line.sku == sku for line in m.lines)
        ]
