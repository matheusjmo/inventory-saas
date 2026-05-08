from fastapi import APIRouter, Depends

from app.api.deps import (
    get_create_product,
    get_get_product,
    get_list_products,
    get_rename_product,
    get_update_price,
)
from app.api.schemas.product import (
    ProductCreateRequest,
    ProductResponse,
    RenameRequest,
    UpdatePriceRequest,
)
from app.application.product.commands import (
    CreateProductCommand,
    RenameProductCommand,
    UpdatePriceCommand,
)
from app.application.product.use_cases import (
    CreateProduct,
    GetProduct,
    ListProducts,
    RenameProduct,
    UpdateProductPrice,
)

router = APIRouter(prefix="/products", tags=["products"])


def _to_response(product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        sku=product.sku.code,
        name=product.name,
        price=product.price.amount,
        currency=product.price.currency,
        category=product.category.name,
    )


@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    body: ProductCreateRequest,
    use_case: CreateProduct = Depends(get_create_product),
):
    product = await use_case.execute(
        CreateProductCommand(
            sku=body.sku,
            name=body.name,
            price=body.price,
            currency=body.currency,
            category=body.category,
        )
    )
    return _to_response(product)


@router.get("", response_model=list[ProductResponse])
async def list_products(use_case: ListProducts = Depends(get_list_products)):
    return [_to_response(p) for p in await use_case.execute()]


@router.get("/{sku}", response_model=ProductResponse)
async def get_product(sku: str, use_case: GetProduct = Depends(get_get_product)):
    return _to_response(await use_case.execute(sku))


@router.patch("/{sku}/price", response_model=ProductResponse)
async def update_price(
    sku: str,
    body: UpdatePriceRequest,
    use_case: UpdateProductPrice = Depends(get_update_price),
):
    product = await use_case.execute(
        UpdatePriceCommand(
            sku=sku, new_price=body.new_price, currency=body.currency
        )
    )
    return _to_response(product)


@router.patch("/{sku}/name", response_model=ProductResponse)
async def rename_product(
    sku: str,
    body: RenameRequest,
    use_case: RenameProduct = Depends(get_rename_product),
):
    product = await use_case.execute(
        RenameProductCommand(sku=sku, new_name=body.new_name)
    )
    return _to_response(product)
