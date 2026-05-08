from decimal import Decimal

import pytest

from app.domain.product.entity import Product
from app.domain.product.value_objects import Category
from app.domain.shared.value_objects import SKU, Price


def make_product(**kwargs) -> Product:
    defaults = dict(
        sku=SKU("SHOE-001"),
        name="Air Max",
        price=Price(Decimal("199.99")),
        category=Category("footwear"),
    )
    return Product(**{**defaults, **kwargs})


def test_sku_is_uppercased():
    assert SKU("shoe-001").code == "SHOE-001"


def test_sku_rejects_invalid():
    with pytest.raises(ValueError):
        SKU("invalid sku!")


def test_price_rejects_negative():
    with pytest.raises(ValueError):
        Price(Decimal("-1"))


def test_category_is_lowercased():
    assert Category("Footwear").name == "footwear"


def test_category_rejects_empty():
    with pytest.raises(ValueError):
        Category("")


def test_product_rename():
    product = make_product()
    product.rename("Air Max 2")
    assert product.name == "Air Max 2"


def test_product_rename_rejects_empty():
    product = make_product()
    with pytest.raises(ValueError):
        product.rename("   ")


def test_product_update_price():
    product = make_product()
    product.update_price(Price(Decimal("299.99")))
    assert product.price.amount == Decimal("299.99")
