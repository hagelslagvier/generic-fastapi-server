from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchemaInput(BaseModel):
    login: str = Field(..., max_length=64)
    password: str = Field(..., max_length=64)
    email: EmailStr
    is_email_confirmed: bool = False
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    is_admin: bool = False


class UserSchemaOutput(UserSchemaInput):
    id: Optional[int]
    created_on: datetime
    updated_on: datetime
