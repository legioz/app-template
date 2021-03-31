from core.databases import Connection
from datetime import datetime, timedelta
from typing import Optional
from core.config import templates, SECRET_KEY
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
        raise HTTPException(status_code=500,detail="Database connection error")
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
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=400,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm=Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/")
async def read_users_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(current_user=Depends(get_current_user)):
    return [{"item_id": "Foo", "owner": current_user['username']}]
