from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.domain.product.value_objects import Category
from app.domain.shared.value_objects import SKU, Price


@dataclass
class Product:
    sku: SKU
    name: str
    price: Price
    category: Category
    id: UUID = field(default_factory=uuid4)

    def update_price(self, new_price: Price) -> None:
        self.price = new_price

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValueError("Product name cannot be empty")
        self.name = new_name.strip()
