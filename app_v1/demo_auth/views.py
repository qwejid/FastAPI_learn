from time import time
from typing import Annotated, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])

security = HTTPBasic()

@router.get('/basic-auth/')
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message":'Hi',
        "username": credentials.username,
        'password': credentials.password,
    }

username_to_password = {
    "admin": 'admin',
    "john": 'password',
}

static_auth_token_to_username = {
    "token1": 'admin',
    "token2": 'john',
}



def get_auth_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = username_to_password.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc
        
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc
    return credentials.username

def get_username_by_static_auth_token(
        static_token: str = Header(alias='x-auth-token')
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Token"},
    )


@router.get('/basic-auth-username/')
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_username)
):    
    return {
        "message":f'Hi {auth_username}',
    }


@router.get('/some-http-header-auth')
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):    
    return {
        "message":f'Hi {username}',
    }

COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web-app-session-id'

def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
        sessoin_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)
) -> dict:
    if sessoin_id not in COOKIES:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    return COOKIES[sessoin_id]

@router.post('/login_cookie')
def demo_auth_login_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_username)
    username: str = Depends(get_username_by_static_auth_token) 
):    
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': username,
        'login_at': int(time())
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    
    return {
        'result': 'ok'
    }

@router.get('/check-cookie/')
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data)
):
    username = user_session_data['username']
    return {
        'message': f'Hi {username}',
        **user_session_data,
    }

@router.get('/logout-cookie')
def demo_auth_logout_cookie(
    response: Response,
    sessoin_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data)
):
    COOKIES.pop(sessoin_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)

    username = user_session_data['username']
    return {
        'message': f'Bye {username}',
    }