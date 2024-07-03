import uvicorn
from fastapi import FastAPI

from api.routers import other, predict

import helpers.lifespan


def set_api() -> FastAPI:
    api = FastAPI(
        title="Inventory planning API",
        lifespan=helpers.lifespan.lifespan,
    )
    api.include_router(router=other.router)
    api.include_router(router=predict.router)

    return api


def run_api() -> None:
    api = set_api()
    uvicorn.run(app=api, host="0.0.0.0", port=8080)
