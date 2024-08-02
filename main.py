from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Query

import uvicorn

from core.config import settings
from core.models import Base, db_helper
from app_v1 import router as routers_v1
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=routers_v1, prefix=settings.api_v1_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {"message": "Hello, World!"}


@app.get("/hello")
def hello_world(name: Annotated[str, Query()] = "world"):
    name = name.strip().title()
    return {"message": f"Hello, {name}!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
