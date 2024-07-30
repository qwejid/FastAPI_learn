from typing import Annotated
from fastapi import FastAPI, Query

from items_views import router as items_router
from users.views import router as users_router

import uvicorn

app = FastAPI()
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
