from pydantic import BaseModel


class ItemPostRequest(BaseModel):
    name: str
    age: int


ItemPutRequest = ItemPostRequest
