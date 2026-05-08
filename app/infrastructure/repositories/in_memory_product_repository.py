from uuid import UUID

from app.domain.product.entity import Product
from app.domain.product.repository import ProductRepository
from app.domain.shared.value_objects import SKU


class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Product] = {}

    async def get_by_sku(self, sku: SKU) -> Product | None:
        return next((p for p in self._store.values() if p.sku == sku), None)

    async def get_by_id(self, id: UUID) -> Product | None:
        return self._store.get(id)

    async def save(self, product: Product) -> None:
        self._store[product.id] = product

    async def list_all(self) -> list[Product]:
        return list(self._store.values())
