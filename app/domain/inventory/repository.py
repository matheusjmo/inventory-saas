from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.stock_movement import StockMovement
from app.domain.shared.value_objects import SKU


class InventoryRepository(ABC):
    @abstractmethod
    async def get_by_sku(self, sku: SKU) -> InventoryItem | None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> InventoryItem | None: ...

    @abstractmethod
    async def save(self, item: InventoryItem) -> None: ...

    @abstractmethod
    async def list_all(self) -> list[InventoryItem]: ...


class StockMovementRepository(ABC):
    @abstractmethod
    async def save(self, movement: StockMovement) -> None: ...

    @abstractmethod
    async def list_by_sku(self, sku: SKU) -> list[StockMovement]: ...
