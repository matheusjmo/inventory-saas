from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class ProductCreateRequest(BaseModel):
    sku: str
    name: str
    price: Decimal
    currency: str = "USD"
    category: str


class UpdatePriceRequest(BaseModel):
    new_price: Decimal
    currency: str = "USD"


class RenameRequest(BaseModel):
    new_name: str


class ProductResponse(BaseModel):
    id: UUID
    sku: str
    name: str
    price: Decimal
    currency: str
    category: str
