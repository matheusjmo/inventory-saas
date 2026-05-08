from fastapi import APIRouter, Depends

from app.api.deps import (
    get_apply_movement,
    get_get_inventory_item,
    get_list_inventory_items,
    get_movement_history,
    get_register_inventory_item,
)
from app.api.schemas.inventory import (
    ApplyMovementRequest,
    InventoryItemResponse,
    MovementLineResponse,
    RegisterInventoryItemRequest,
    StockMovementResponse,
)
from app.application.inventory.commands import (
    ApplyMovementCommand,
    MovementLineCommand,
    RegisterInventoryItemCommand,
)
from app.application.inventory.use_cases import (
    ApplyStockMovement,
    GetInventoryItem,
    GetMovementHistory,
    ListInventoryItems,
    RegisterInventoryItem,
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


def _item_to_response(item) -> InventoryItemResponse:
    return InventoryItemResponse(
        id=item.id,
        sku=item.sku.code,
        quantity=item.quantity.value,
        unit=item.quantity.unit,
    )


def _movement_to_response(movement) -> StockMovementResponse:
    return StockMovementResponse(
        id=movement.id,
        type=movement.type.value,
        lines=[
            MovementLineResponse(sku=line.sku.code, quantity=line.quantity.value)
            for line in movement.lines
        ],
        occurred_at=movement.occurred_at,
    )


@router.post("", response_model=InventoryItemResponse, status_code=201)
async def register_inventory_item(
    body: RegisterInventoryItemRequest,
    use_case: RegisterInventoryItem = Depends(get_register_inventory_item),
):
    item = await use_case.execute(
        RegisterInventoryItemCommand(
            sku=body.sku,
            initial_quantity=body.initial_quantity,
            unit=body.unit,
        )
    )
    return _item_to_response(item)


@router.get("", response_model=list[InventoryItemResponse])
async def list_inventory_items(
    limit: int = 20,
    offset: int = 0,
    use_case: ListInventoryItems = Depends(get_list_inventory_items),
):
    return [
        _item_to_response(i)
        for i in await use_case.execute(limit=limit, offset=offset)
    ]


@router.get("/{sku}", response_model=InventoryItemResponse)
async def get_inventory_item(
    sku: str,
    use_case: GetInventoryItem = Depends(get_get_inventory_item),
):
    return _item_to_response(await use_case.execute(sku))


@router.post("/movements", response_model=list[InventoryItemResponse], status_code=201)
async def apply_movement(
    body: ApplyMovementRequest,
    use_case: ApplyStockMovement = Depends(get_apply_movement),
):
    items = await use_case.execute(
        ApplyMovementCommand(
            movement_type=body.movement_type,
            lines=[
                MovementLineCommand(sku=line.sku, quantity=line.quantity)
                for line in body.lines
            ],
        )
    )
    return [_item_to_response(i) for i in items]


@router.get("/{sku}/movements", response_model=list[StockMovementResponse])
async def get_movement_history(
    sku: str,
    use_case: GetMovementHistory = Depends(get_movement_history),
):
    movements = await use_case.execute(sku)
    return [_movement_to_response(m) for m in movements]
