from httpx import AsyncClient

PRODUCT_PAYLOAD = {
    "sku": "SHOE-001",
    "name": "Air Max",
    "price": "199.99",
    "currency": "USD",
    "category": "footwear",
}


async def _create_product_and_item(
    client: AsyncClient, sku: str = "SHOE-001", qty: int = 0
):
    payload = {**PRODUCT_PAYLOAD, "sku": sku}
    await client.post("/products", json=payload)
    await client.post("/inventory", json={"sku": sku, "initial_quantity": qty})


async def test_register_inventory_item(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.post(
        "/inventory", json={"sku": "SHOE-001", "initial_quantity": 0}
    )
    assert response.status_code == 201
    assert response.json()["sku"] == "SHOE-001"
    assert response.json()["quantity"] == 0


async def test_register_inventory_item_product_not_found(client: AsyncClient):
    response = await client.post(
        "/inventory", json={"sku": "NOTEXIST", "initial_quantity": 0}
    )
    assert response.status_code == 404


async def test_register_inventory_item_duplicate(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    await client.post("/inventory", json={"sku": "SHOE-001", "initial_quantity": 0})
    response = await client.post(
        "/inventory", json={"sku": "SHOE-001", "initial_quantity": 0}
    )
    assert response.status_code == 409


async def test_list_inventory_items(client: AsyncClient):
    await _create_product_and_item(client)
    response = await client.get("/inventory")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_inventory_item(client: AsyncClient):
    await _create_product_and_item(client, qty=10)
    response = await client.get("/inventory/SHOE-001")
    assert response.status_code == 200
    assert response.json()["quantity"] == 10


async def test_apply_movement_in(client: AsyncClient):
    await _create_product_and_item(client, qty=10)
    response = await client.post(
        "/inventory/movements",
        json={"movement_type": "in", "lines": [{"sku": "SHOE-001", "quantity": 5}]},
    )
    assert response.status_code == 201
    assert response.json()[0]["quantity"] == 15


async def test_apply_movement_out(client: AsyncClient):
    await _create_product_and_item(client, qty=10)
    response = await client.post(
        "/inventory/movements",
        json={"movement_type": "out", "lines": [{"sku": "SHOE-001", "quantity": 3}]},
    )
    assert response.status_code == 201
    assert response.json()[0]["quantity"] == 7


async def test_apply_movement_out_insufficient_stock(client: AsyncClient):
    await _create_product_and_item(client, qty=5)
    response = await client.post(
        "/inventory/movements",
        json={"movement_type": "out", "lines": [{"sku": "SHOE-001", "quantity": 10}]},
    )
    assert response.status_code == 422


async def test_get_movement_history(client: AsyncClient):
    await _create_product_and_item(client, qty=10)
    await client.post(
        "/inventory/movements",
        json={"movement_type": "in", "lines": [{"sku": "SHOE-001", "quantity": 5}]},
    )
    response = await client.get("/inventory/SHOE-001/movements")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["type"] == "in"
