import pytest

from app.domain.exceptions import DomainValidationError
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.stock_movement import MovementLine, StockMovement
from app.domain.inventory.value_objects import MovementType, Quantity
from app.domain.shared.value_objects import SKU


def make_item(quantity: int = 10) -> InventoryItem:
    return InventoryItem(sku=SKU("SHOE-001"), quantity=Quantity(quantity))


def test_quantity_rejects_negative():
    with pytest.raises(ValueError):
        Quantity(-1)


def test_quantity_add():
    assert (Quantity(10) + Quantity(5)).value == 15


def test_quantity_sub():
    assert (Quantity(10) - Quantity(5)).value == 5


def test_quantity_sub_rejects_going_negative():
    with pytest.raises(DomainValidationError):
        Quantity(5) - Quantity(10)


def test_apply_movement_in():
    item = make_item(10)
    item.apply(Quantity(5), MovementType.IN)
    assert item.quantity.value == 15


def test_apply_movement_out():
    item = make_item(10)
    item.apply(Quantity(5), MovementType.OUT)
    assert item.quantity.value == 5


def test_apply_movement_adjustment():
    item = make_item(10)
    item.apply(Quantity(3), MovementType.ADJUSTMENT)
    assert item.quantity.value == 3


def test_apply_movement_out_cannot_go_negative():
    item = make_item(5)
    with pytest.raises(DomainValidationError):
        item.apply(Quantity(10), MovementType.OUT)


def test_stock_movement_rejects_empty_lines():
    with pytest.raises(ValueError):
        StockMovement(type=MovementType.IN, lines=[])


def test_stock_movement_has_timestamp():
    movement = StockMovement(
        type=MovementType.IN,
        lines=[MovementLine(sku=SKU("SHOE-001"), quantity=Quantity(5))],
    )
    assert movement.occurred_at is not None
