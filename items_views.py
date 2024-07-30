from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

@router.get("/")
def list_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]


@router.get("/latest")
def get_latest():
    return {'item': {'id': '0', 'name': 'latest'}}

@router.get("/{item_id}")
def get_item(item_id: Annotated[int, Path(ge=1, lt=1_000_000)]):
    return {"id": item_id, "name": f"Item {item_id}"}