from app.domain.exceptions import NotFoundError
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.repository import InventoryRepository, StockMovementRepository
from app.domain.inventory.stock_movement import StockMovement


class InventoryDomainService:
    def __init__(
        self,
        inventory_repo: InventoryRepository,
        movement_repo: StockMovementRepository,
    ) -> None:
        self._inventory_repo = inventory_repo
        self._movement_repo = movement_repo

    async def apply_movement(self, movement: StockMovement) -> list[InventoryItem]:
        affected = []
        for line in movement.lines:
            item = await self._inventory_repo.get_by_sku(line.sku)
            if item is None:
                raise NotFoundError(f"No inventory item found for SKU {line.sku.code}")
            item.apply(line.quantity, movement.type)
            await self._inventory_repo.save(item)
            affected.append(item)
        await self._movement_repo.save(movement)
        return affected
