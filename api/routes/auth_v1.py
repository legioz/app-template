from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import JSONResponse
from core.config import AuthJWT, SECRET_KEY
from core.databases import Connection
from passlib.hash import bcrypt

router = APIRouter()


Settings = [
    ('authjwt_secret_key', SECRET_KEY),
    ('authjwt_algorithm', 'HS512'),
    ('authjwt_token_location', {"cookies"}),
    ('authjwt_cookie_csrf_protect', True),
]


@AuthJWT.load_config
def get_config():
    return Settings


@router.post('/login', name='login_for_access_token')
def login(username: str=Form(...), password: str=Form(...), Authorize: AuthJWT=Depends()):
    try:
        with Connection() as db:
            sql = 'SELECT * FROM auth_user WHERE username = %s LIMIT 1'
            result = db.query_dict(sql, [username])
    except Exception:
        raise HTTPException(status_code=500,detail="Database connection error")
    if not result:
        raise HTTPException(status_code=401,detail="Bad username")
    if not bcrypt.verify(password, result[0]['password']):
        raise HTTPException(status_code=401,detail="Bad username or password")

    # Create the tokens and passing to set_access_cookies or set_refresh_cookies
    access_token = Authorize.create_access_token(subject=username)
    refresh_token = Authorize.create_refresh_token(subject=username)

    # Set the JWT cookies in the response
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {"msg":"Successfully login"}


@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}


@router.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


