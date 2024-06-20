from pydantic import BaseModel


class Item(BaseModel):
    uuid: str
    name: str
    age: int
