from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routers import inventory, products
from app.domain.exceptions import (
    AlreadyExistsError,
    DomainValidationError,
    NotFoundError,
)

app = FastAPI(title="Inventory SaaS API")

app.include_router(products.router)
app.include_router(inventory.router)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AlreadyExistsError)
async def already_exists_handler(
    request: Request, exc: AlreadyExistsError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(DomainValidationError)
async def validation_handler(
    request: Request, exc: DomainValidationError
) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})
