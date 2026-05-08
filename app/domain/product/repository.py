from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.product.entity import Product
from app.domain.shared.value_objects import SKU


class ProductRepository(ABC):
    @abstractmethod
    async def get_by_sku(self, sku: SKU) -> Product | None: ...

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Product | None: ...

    @abstractmethod
    async def save(self, product: Product) -> None: ...

    @abstractmethod
    async def list_all(self) -> list[Product]: ...
