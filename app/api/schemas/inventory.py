from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RegisterInventoryItemRequest(BaseModel):
    sku: str
    initial_quantity: int = 0
    unit: str = "units"


class InventoryItemResponse(BaseModel):
    id: UUID
    sku: str
    quantity: int
    unit: str


class MovementLineRequest(BaseModel):
    sku: str
    quantity: int


class ApplyMovementRequest(BaseModel):
    movement_type: str  # "in", "out", "adjustment"
    lines: list[MovementLineRequest]


class MovementLineResponse(BaseModel):
    sku: str
    quantity: int


class StockMovementResponse(BaseModel):
    id: UUID
    type: str
    lines: list[MovementLineResponse]
    occurred_at: datetime
