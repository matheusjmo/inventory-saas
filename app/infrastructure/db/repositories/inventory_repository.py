from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.repository import InventoryRepository, StockMovementRepository
from app.domain.inventory.stock_movement import MovementLine, StockMovement
from app.domain.inventory.value_objects import MovementType, Quantity
from app.domain.shared.value_objects import SKU
from app.infrastructure.db.models.inventory import (
    InventoryItemORM,
    MovementLineORM,
    StockMovementORM,
)


def _item_to_domain(row: InventoryItemORM) -> InventoryItem:
    return InventoryItem(
        id=row.id,
        sku=SKU(row.sku),
        quantity=Quantity(value=row.quantity, unit=row.unit),
    )


def _movement_to_domain(row: StockMovementORM) -> StockMovement:
    return StockMovement(
        id=row.id,
        type=MovementType(row.type),
        occurred_at=row.occurred_at,
        lines=[
            MovementLine(
                sku=SKU(line.sku),
                quantity=Quantity(value=line.quantity, unit=line.unit),
            )
            for line in row.lines
        ],
    )


class SqlInventoryRepository(InventoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_sku(self, sku: SKU) -> InventoryItem | None:
        result = await self._session.execute(
            select(InventoryItemORM).where(InventoryItemORM.sku == sku.code)
        )
        row = result.scalar_one_or_none()
        return _item_to_domain(row) if row else None

    async def get_by_id(self, id: UUID) -> InventoryItem | None:
        result = await self._session.execute(
            select(InventoryItemORM).where(InventoryItemORM.id == id)
        )
        row = result.scalar_one_or_none()
        return _item_to_domain(row) if row else None

    async def save(self, item: InventoryItem) -> None:
        result = await self._session.execute(
            select(InventoryItemORM).where(InventoryItemORM.id == item.id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            self._session.add(InventoryItemORM(
                id=item.id,
                sku=item.sku.code,
                quantity=item.quantity.value,
                unit=item.quantity.unit,
            ))
        else:
            row.quantity = item.quantity.value
            row.unit = item.quantity.unit

    async def list_all(self) -> list[InventoryItem]:
        result = await self._session.execute(select(InventoryItemORM))
        return [_item_to_domain(row) for row in result.scalars().all()]


class SqlStockMovementRepository(StockMovementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, movement: StockMovement) -> None:
        orm = StockMovementORM(
            id=movement.id,
            type=movement.type.value,
            occurred_at=movement.occurred_at,
            lines=[
                MovementLineORM(
                    sku=line.sku.code,
                    quantity=line.quantity.value,
                    unit=line.quantity.unit,
                )
                for line in movement.lines
            ],
        )
        self._session.add(orm)

    async def list_by_sku(self, sku: SKU) -> list[StockMovement]:
        result = await self._session.execute(
            select(StockMovementORM)
            .join(MovementLineORM)
            .where(MovementLineORM.sku == sku.code)
            .options(selectinload(StockMovementORM.lines))
        )
        return [_movement_to_domain(row) for row in result.scalars().all()]
