from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product.entity import Product
from app.domain.product.repository import ProductRepository
from app.domain.product.value_objects import Category
from app.domain.shared.value_objects import Price, SKU
from app.infrastructure.db.models.product import ProductORM


def _to_domain(row: ProductORM) -> Product:
    return Product(
        id=row.id,
        sku=SKU(row.sku),
        name=row.name,
        price=Price(amount=row.price, currency=row.currency),
        category=Category(row.category),
    )


def _to_orm(product: Product) -> ProductORM:
    return ProductORM(
        id=product.id,
        sku=product.sku.code,
        name=product.name,
        price=product.price.amount,
        currency=product.price.currency,
        category=product.category.name,
    )


class SqlProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_sku(self, sku: SKU) -> Product | None:
        result = await self._session.execute(
            select(ProductORM).where(ProductORM.sku == sku.code)
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def get_by_id(self, id: UUID) -> Product | None:
        result = await self._session.execute(
            select(ProductORM).where(ProductORM.id == id)
        )
        row = result.scalar_one_or_none()
        return _to_domain(row) if row else None

    async def save(self, product: Product) -> None:
        result = await self._session.execute(
            select(ProductORM).where(ProductORM.id == product.id)
        )
        row = result.scalar_one_or_none()
        if row is None:
            self._session.add(_to_orm(product))
        else:
            row.sku = product.sku.code
            row.name = product.name
            row.price = product.price.amount
            row.currency = product.price.currency
            row.category = product.category.name

    async def list_all(self) -> list[Product]:
        result = await self._session.execute(select(ProductORM))
        return [_to_domain(row) for row in result.scalars().all()]
