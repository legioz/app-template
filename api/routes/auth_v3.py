from core.databases import Connection
from datetime import datetime, timedelta
from typing import Optional
from core.config import templates, SECRET_KEY
from fastapi import Depends, APIRouter, HTTPException, Response, Cookie, Form
from fastapi.security import APIKeyCookie,
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

cookie_sec = APIKeyCookie(name='session')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    user = None
    with Connection() as db:
            sql = 'SELECT * FROM auth_user WHERE username = %s AND is_active = 1 LIMIT 1'
            result = db.query_dict(sql, [username])
            user = result[0]
    return user


def authenticate_user(username: str, password: str):
    user = None
    try:
        with Connection() as db:
            sql = 'SELECT * FROM auth_user WHERE username = %s AND is_active = 1 LIMIT 1'
            result = db.query_dict(sql, [username])
            user = result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500,detail='Database connection error')
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(session: str = Depends(cookie_sec)):
    credentials_exception = HTTPException(
        status_code=400,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(session, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    # ! código pra realizar SELECT e verificar se a sessão está ativa e se a session_key
    sqlValidaSessao = """
        SELECT *
        FROM auth_session
        WHERE session_key = %s
        AND expire_date > NOW()
    """
    return user


@router.post('/login')
async def login_for_access_token(response: Response, username: str=Form(...), password: str=Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # ! código pra inserir sessão no DB -> tabela auth_session(id, session_key, session_data, expire_date)
        # ! session_key -> chave randômica unica
        # ! session_data -> JWT contendo usuário
        data={'sub': user['username']}, expires_delta=access_token_expires
    )
    response.set_cookie('session', access_token, httponly=True)
    return {'ok': True}


@router.delete('/logout')
async def logout(response: Response):
    # ! deleta o registro da tabela auth_session
    response.delete_cookie('session')
    return {'ok': True}


@router.get('/users/me/')
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user

