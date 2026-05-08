from fastapi import FastAPI

from app.api.routers import inventory, products

app = FastAPI(title="Inventory SaaS API")

app.include_router(products.router)
app.include_router(inventory.router)
