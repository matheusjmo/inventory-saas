from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CreateProductCommand:
    sku: str
    name: str
    price: Decimal
    currency: str
    category: str


@dataclass
class UpdatePriceCommand:
    sku: str
    new_price: Decimal
    currency: str


@dataclass
class RenameProductCommand:
    sku: str
    new_name: str
