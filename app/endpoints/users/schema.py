from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchemaInput(BaseModel):
    login: str
    password: str
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    is_admin: bool = False


class UserSchemaOutput(UserSchemaInput):
    id: Optional[int]
    created_on: datetime
    updated_on: datetime
