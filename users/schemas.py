from typing import Annotated
from fastapi import Body
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, ConfigDict


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: Annotated[EmailStr, Body()]

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool =True
