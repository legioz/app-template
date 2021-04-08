from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.databases import Connection
from core.config import SECRET_KEY
import secrets
from passlib import pwd

router = APIRouter()

ALGORITHM = 'HS512'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 10
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_new_session_key():
    return secrets.token_urlsafe(20) + pwd.genword(entropy=100, length=20)


def get_password_hash(password):
    return pwd_context.hash(password)


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
        raise HTTPException(status_code=500, detail='Database connection error')
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
    to_encode.update({'exp': expire, 'iat': datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        with Connection() as db:
            sql = '''
                SELECT * 
                FROM auth_session 
                WHERE access_token = %s 
                    AND expire_date > NOW()
                LIMIT 1
            ''' 
            result = db.query_dict(sql, [token])
            if not result:
                raise credentials_exception
            else:
                if result[0]['access_token'] != token:
                    raise credentials_exception
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def save_session(user, access_token):
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
                    access_token = %s,
                    expire_date = NOW() + INTERVAL %s MINUTE
                    WHERE user_id = %s
                '''
                db.execute(sqlUpdateTokenExistente, [access_token, ACCESS_TOKEN_EXPIRE_MINUTES, user['id']])
            else:
                sqlInsertSession = '''
                    INSERT INTO auth_session 
                    (user_id, access_token, expire_date) VALUES 
                    (%s, %s, NOW() + INTERVAL %s MINUTE)
                '''
                db.execute(sqlInsertSession, [user['id'], access_token, ACCESS_TOKEN_EXPIRE_MINUTES])
    except Exception:
        raise HTTPException(status_code=500, detail='Internal server error while connecting')


@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    '''
    Create **access token** and save session to database. 
    '''
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user['username'], 'randkey': create_new_session_key()}, 
        expires_delta=access_token_expires
    )
    await save_session(user, access_token)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.put('/token/refresh')
async def refresh_for_access_token(current_user=Depends(get_current_user)):
    '''
    Update **access token** on headers and update session on database. 
    '''
    user = current_user
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect username or password', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user['username'], 'randkey': create_new_session_key()}, 
        expires_delta=access_token_expires
    )
    save_session(user, access_token)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete('/logout', name='auth_v1:logout')
async def logout(current_user=Depends(get_current_user)):
    '''
    Delete session on database. 
    '''
    credentials_exception = HTTPException(
        status_code=400,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        with Connection() as db:
            db.execute('DELETE FROM auth_session WHERE user_id = %s', [current_user['id']])
    except JWTError:
        raise credentials_exception
    return {'ok': True}


@router.get("/users/me/")
async def read_users_me(current_user=Depends(get_current_user)):
    '''
    Return current user info.
    '''
    return current_user
