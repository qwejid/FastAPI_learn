from users.schemas import CreateUser
from fastapi import APIRouter
from users import crud

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user: CreateUser):
    return crud.creat_user(user_in=user)
