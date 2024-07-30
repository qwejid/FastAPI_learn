from users.schemas import CreateUser


def creat_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {
        'success': True,
        'user': user,
    }