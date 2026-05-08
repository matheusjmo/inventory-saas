import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.infrastructure.db.session import AsyncSessionFactory
from app.main import app


@pytest.fixture(autouse=True)
async def clean_tables():
    async with AsyncSessionFactory() as session:
        await session.execute(
            text(
                "TRUNCATE movement_lines, stock_movements, "
                "inventory_items, products RESTART IDENTITY CASCADE"
            )
        )
        await session.commit()
    yield


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
