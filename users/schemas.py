from typing import Annotated
from fastapi import Body
from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: Annotated[EmailStr, Body()]


class DeleteUser(BaseModel):
    pass
