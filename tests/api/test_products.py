from httpx import AsyncClient

PRODUCT_PAYLOAD = {
    "sku": "SHOE-001",
    "name": "Air Max",
    "price": "199.99",
    "currency": "USD",
    "category": "footwear",
}


async def test_create_product(client: AsyncClient):
    response = await client.post("/products", json=PRODUCT_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "SHOE-001"
    assert data["name"] == "Air Max"
    assert data["category"] == "footwear"


async def test_create_product_duplicate_sku(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.post("/products", json=PRODUCT_PAYLOAD)
    assert response.status_code == 409


async def test_list_products_empty(client: AsyncClient):
    response = await client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


async def test_list_products(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_product(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.get("/products/SHOE-001")
    assert response.status_code == 200
    assert response.json()["sku"] == "SHOE-001"


async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/products/NOTEXIST")
    assert response.status_code == 404


async def test_update_price(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.patch(
        "/products/SHOE-001/price",
        json={"new_price": "299.99", "currency": "USD"},
    )
    assert response.status_code == 200
    assert response.json()["price"] == "299.99"


async def test_rename_product(client: AsyncClient):
    await client.post("/products", json=PRODUCT_PAYLOAD)
    response = await client.patch(
        "/products/SHOE-001/name", json={"new_name": "Air Max 2"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Air Max 2"
