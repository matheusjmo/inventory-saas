from app.domain.exceptions import AlreadyExistsError, NotFoundError
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.repository import InventoryRepository, StockMovementRepository
from app.domain.inventory.service import InventoryDomainService
from app.domain.inventory.stock_movement import MovementLine, StockMovement
from app.domain.inventory.value_objects import MovementType, Quantity
from app.domain.product.repository import ProductRepository
from app.domain.shared.value_objects import SKU

from .commands import ApplyMovementCommand, RegisterInventoryItemCommand


class RegisterInventoryItem:
    def __init__(
        self,
        inventory_repo: InventoryRepository,
        product_repo: ProductRepository,
    ) -> None:
        self._inventory_repo = inventory_repo
        self._product_repo = product_repo

    async def execute(self, cmd: RegisterInventoryItemCommand) -> InventoryItem:
        sku = SKU(cmd.sku)

        if await self._product_repo.get_by_sku(sku) is None:
            raise NotFoundError(f"Product with SKU {sku.code} not found")

        if await self._inventory_repo.get_by_sku(sku) is not None:
            raise AlreadyExistsError(
                f"Inventory item for SKU {sku.code} already exists"
            )

        item = InventoryItem(
            sku=sku,
            quantity=Quantity(value=cmd.initial_quantity, unit=cmd.unit),
        )
        await self._inventory_repo.save(item)
        return item


class ApplyStockMovement:
    def __init__(
        self,
        inventory_repo: InventoryRepository,
        movement_repo: StockMovementRepository,
    ) -> None:
        self._service = InventoryDomainService(inventory_repo, movement_repo)

    async def execute(self, cmd: ApplyMovementCommand) -> list[InventoryItem]:
        movement = StockMovement(
            type=MovementType(cmd.movement_type),
            lines=[
                MovementLine(sku=SKU(line.sku), quantity=Quantity(line.quantity))
                for line in cmd.lines
            ],
        )
        return await self._service.apply_movement(movement)


class GetInventoryItem:
    def __init__(self, repo: InventoryRepository) -> None:
        self._repo = repo

    async def execute(self, sku: str) -> InventoryItem:
        item = await self._repo.get_by_sku(SKU(sku))
        if item is None:
            raise NotFoundError(f"No inventory item found for SKU {sku}")
        return item


class ListInventoryItems:
    def __init__(self, repo: InventoryRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[InventoryItem]:
        return await self._repo.list_all()


class GetMovementHistory:
    def __init__(self, repo: StockMovementRepository) -> None:
        self._repo = repo

    async def execute(self, sku: str) -> list[StockMovement]:
        return await self._repo.list_by_sku(SKU(sku))
