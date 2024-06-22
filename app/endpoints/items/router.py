import json
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import NonNegativeInt

from app.endpoints.items.schema.requests import ItemPostRequest, ItemPutRequest
from app.endpoints.items.schema.responses import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("/")
def create(item: ItemPostRequest) -> Item:
    import json
    import random

    payload = item.dict()
    payload.update({"uuid": str(random.randint(100, 1000))})

    response_item = Item(**payload)

    print(f"Create: {json.dumps(response_item.dict(), indent=4)}")

    return response_item


@router.get("/{uuid}")
def read_one(uuid: str) -> Item:
    from dataclasses import asdict

    from app.db.fake import items

    if not (storage_item := items.get(uuid, None)):
        raise HTTPException(status_code=404, detail=f"Item with uuid={uuid} not found")

    response_item = Item(**asdict(storage_item))

    print(
        f"Read one: {json.dumps(response_item.dict(), indent=4) if response_item else response_item}"
    )

    return response_item


@router.get("/")
def read_many(skip: NonNegativeInt = 0, take: int = 5) -> List[Item]:
    from dataclasses import asdict

    from app.db.fake import items

    storage_items = [
        items[k] for index, k in enumerate(items) if skip <= index < skip + take
    ]
    response_items = [Item(**asdict(item)) for item in storage_items]

    return response_items


@router.put("/{uuid}")
def update(uuid: str, item: ItemPutRequest) -> Item:
    import json
    from dataclasses import asdict

    from app.db.fake import items

    if not (storage_item := items.get(uuid, None)):
        raise HTTPException(status_code=404, detail=f"Item with uuid={uuid} not found")

    payload = item.dict()
    new_storage_item = asdict(storage_item)
    new_storage_item.update(**payload)

    response_item = Item(**new_storage_item)
    print(f"Update one: {json.dumps(response_item.dict(), indent=4) if item else item}")
    return response_item


@router.delete("/{uuid}")
def delete(uuid: str) -> Item:
    from dataclasses import asdict

    from app.db.fake import items

    if not (storage_item := items.get(uuid, None)):
        raise HTTPException(status_code=404, detail=f"Item with uuid={uuid} not found")

    response_item = Item(**asdict(storage_item))
    print(
        f"Delete one: {json.dumps(response_item.dict(), indent=4) if response_item else response_item}"
    )
    return response_item
