from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.inventory.use_cases import (
    ApplyStockMovement,
    GetInventoryItem,
    GetMovementHistory,
    ListInventoryItems,
    RegisterInventoryItem,
)
from app.application.product.use_cases import (
    CreateProduct,
    GetProduct,
    ListProducts,
    RenameProduct,
    UpdateProductPrice,
)
from app.infrastructure.db.repositories.inventory_repository import (
    SqlInventoryRepository,
    SqlStockMovementRepository,
)
from app.infrastructure.db.repositories.product_repository import SqlProductRepository
from app.infrastructure.db.session import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_create_product(session: SessionDep) -> CreateProduct:
    return CreateProduct(SqlProductRepository(session))


def get_update_price(session: SessionDep) -> UpdateProductPrice:
    return UpdateProductPrice(SqlProductRepository(session))


def get_rename_product(session: SessionDep) -> RenameProduct:
    return RenameProduct(SqlProductRepository(session))


def get_list_products(session: SessionDep) -> ListProducts:
    return ListProducts(SqlProductRepository(session))


def get_get_product(session: SessionDep) -> GetProduct:
    return GetProduct(SqlProductRepository(session))


def get_register_inventory_item(session: SessionDep) -> RegisterInventoryItem:
    return RegisterInventoryItem(SqlInventoryRepository(session), SqlProductRepository(session))


def get_apply_movement(session: SessionDep) -> ApplyStockMovement:
    return ApplyStockMovement(SqlInventoryRepository(session), SqlStockMovementRepository(session))


def get_get_inventory_item(session: SessionDep) -> GetInventoryItem:
    return GetInventoryItem(SqlInventoryRepository(session))


def get_list_inventory_items(session: SessionDep) -> ListInventoryItems:
    return ListInventoryItems(SqlInventoryRepository(session))


def get_movement_history(session: SessionDep) -> GetMovementHistory:
    return GetMovementHistory(SqlStockMovementRepository(session))
