from core.databases import Connection
from datetime import datetime, timedelta
from typing import Dict, Optional
from core.config import templates, SECRET_KEY
from fastapi import Depends, APIRouter, HTTPException, Response, Cookie, Form, Request
from fastapi.security import OAuth2
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
from passlib import pwd
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from calendar import timegm
from datetime import datetime

router = APIRouter()


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")
        if not authorization:
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return authorization


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='/token', scheme_name='bearer')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_new_session_key():
    return secrets.token_urlsafe(20) + pwd.genword(entropy=100, length=20)


def get_user(username: str):
    user = None
    with Connection() as db:
            sql = 'SELECT * FROM auth_user WHERE username = %s AND is_active = 1 LIMIT 1'
            result = db.query_dict(sql, [username])
            user = result[0] if result else None
    return user


def authenticate_user(username: str, password: str):
    try:
        user = get_user(username)
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


async def get_current_user(authorization: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=400,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        session_key: str = payload.get('sesskey')
        utc_now = timegm(datetime.utcnow().utctimetuple())
        if payload['exp'] <= utc_now:
            raise HTTPException(401, detail='Credentials have expired')
        if username is None or session_key is None:
            raise credentials_exception
        with Connection() as db:
            sql = '''
                SELECT * 
                FROM auth_session 
                WHERE session_key = %s 
                    AND expire_date > NOW()  
                LIMIT 1
            ''' 
            result = db.query_dict(sql, [session_key])
            if not result:
                raise HTTPException(status_code=400, detail='Credentials have expired')
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post('/token')
async def login_for_access_token(response: Response, username: str=Form(...), password: str=Form(...)):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    session_key = create_new_session_key()
    access_token = create_access_token(
        data={'sub': user['username'], 'sesskey': session_key}, expires_delta=access_token_expires
    )
    try:
        with Connection() as db:
            db.execute('UPDATE auth_user SET last_login = NOW() WHERE id = %s', [user['id']])
            sqlValidaTokenExistente = '''
                SELECT * 
                FROM auth_session a 
                INNER JOIN auth_user b ON a.user_id = b.id
                WHERE b.username = %s
                LIMIT 1
            '''
            resultTokenExistente = db.query_dict(sqlValidaTokenExistente, [user['username']])
            if resultTokenExistente:
                sqlUpdateTokenExistente = '''
                    UPDATE auth_session
                    SET
                    session_key = %s,
                    expire_date = NOW() + INTERVAL %s MINUTE
                    WHERE user_id = %s
                '''
                db.execute(sqlUpdateTokenExistente, [session_key, ACCESS_TOKEN_EXPIRE_MINUTES, user['id']])
            else:
                db.execute('INSERT INTO auth_session (user_id, session_key, expire_date) VALUES (%s, %s, NOW() + INTERVAL %s MINUTE)', [user['id'], session_key, ACCESS_TOKEN_EXPIRE_MINUTES])
    except Exception:
        raise HTTPException(status_code=500,detail='Insert Login Error')
    response.set_cookie('access_token', access_token, httponly=True)
    return {'ok': True}


@router.post('/refresh')
async def refresh_for_access_token(response: Response, request: Request, user=Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=400,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        # ! Velho Token
        access_token = request.cookies.get('access_token')
        if not access_token:
            raise credentials_exception
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session_key: str = payload.get('sesskey')
        # ! Novo Token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_session_key = create_new_session_key()
        new_access_token = create_access_token(
            data={'sub': user['username'], 'sesskey': new_session_key}, expires_delta=access_token_expires
        )
        if session_key is None:
            raise credentials_exception
        with Connection() as db:
            sqlUpdateTokenExistente = '''
                    UPDATE auth_session
                    SET
                    session_key = %s,
                    expire_date = NOW() + INTERVAL %s MINUTE
                    WHERE user_id = %s
                '''
            db.execute(sqlUpdateTokenExistente, [new_session_key, ACCESS_TOKEN_EXPIRE_MINUTES, user['id']])
    except JWTError:
        raise credentials_exception
    response.delete_cookie('access_token')
    response.set_cookie('access_token', new_access_token, httponly=True)
    return {'ok': True}


@router.delete('/logout')
async def logout(response: Response, request: Request):
    credentials_exception = HTTPException(
        status_code=400,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        access_token = request.cookies.get('access_token')
        if not access_token:
            raise credentials_exception
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        session_key: str = payload.get('sesskey')
        if session_key is None:
            raise credentials_exception
        with Connection() as db:
            db.execute('DELETE FROM auth_session WHERE session_key = %s', [session_key])
    except JWTError:
        raise credentials_exception
    response.delete_cookie('access_token')
    return {'ok': True}


@router.get('/users/me/')
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user
