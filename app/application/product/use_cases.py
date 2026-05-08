from app.domain.product.entity import Product
from app.domain.product.repository import ProductRepository
from app.domain.product.value_objects import Category
from app.domain.shared.value_objects import SKU, Price

from .commands import CreateProductCommand, RenameProductCommand, UpdatePriceCommand


class CreateProduct:
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    async def execute(self, cmd: CreateProductCommand) -> Product:
        sku = SKU(cmd.sku)
        if await self._repo.get_by_sku(sku) is not None:
            raise ValueError(f"Product with SKU {sku.code} already exists")

        product = Product(
            sku=sku,
            name=cmd.name,
            price=Price(amount=cmd.price, currency=cmd.currency),
            category=Category(name=cmd.category),
        )
        await self._repo.save(product)
        return product


class UpdateProductPrice:
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    async def execute(self, cmd: UpdatePriceCommand) -> Product:
        product = await self._repo.get_by_sku(SKU(cmd.sku))
        if product is None:
            raise ValueError(f"Product with SKU {cmd.sku} not found")

        product.update_price(Price(amount=cmd.new_price, currency=cmd.currency))
        await self._repo.save(product)
        return product


class RenameProduct:
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    async def execute(self, cmd: RenameProductCommand) -> Product:
        product = await self._repo.get_by_sku(SKU(cmd.sku))
        if product is None:
            raise ValueError(f"Product with SKU {cmd.sku} not found")

        product.rename(cmd.new_name)
        await self._repo.save(product)
        return product


class ListProducts:
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[Product]:
        return await self._repo.list_all()


class GetProduct:
    def __init__(self, repo: ProductRepository) -> None:
        self._repo = repo

    async def execute(self, sku: str) -> Product:
        product = await self._repo.get_by_sku(SKU(sku))
        if product is None:
            raise ValueError(f"Product with SKU {sku} not found")
        return product
