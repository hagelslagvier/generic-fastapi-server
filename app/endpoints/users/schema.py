from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserSchemaInput(BaseModel):
    login: str = Field(..., max_length=64)
    password: str = Field(..., max_length=64)
    email: EmailStr
    is_email_confirmed: bool = False
    refresh_token: str | None = None
    access_token: str | None = None
    is_admin: bool = False


class UserSchemaOutput(UserSchemaInput):
    id: int
    created_on: datetime
    updated_on: datetime
