import mariadb
from dotenv import load_dotenv, find_dotenv
import os
from typing import Any
from functools import wraps
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')
PROJECT_NAME = os.getenv('PROJECT_NAME')
DEBUG = os.getenv('DEBUG')
MARIADB_USER = os.getenv('MARIADB_USER')
MARIADB_PASS = os.getenv('MARIADB_PASS')
MARIADB_HOST = os.getenv('MARIADB_HOST')
MARIADB_DB = os.getenv('MARIADB_DB')


def load_user(user):
    return user

# from fastapi_redis_session.config import basicConfig
# basicConfig(
#     redisURL="redis://redis:6379/1",
#     )

# with Database('database') as db:
#     res = db.query_dict('SELECT top 1 * FROM database')
#     print(res[0]['DT_INGRESSO'])


# def decorator(funcao):
#     def wrapper():
#         print ("Estou antes da execução da função passada como argumento")
#         funcao()
#         print ("Estou depois da execução da função passada como argumento")

#     return wrapper


# # ! Decorator
# def logged_in(f):
#     @wraps(f)
#     def funcao_decorada(*args, **kwargs):
#         # Verifica session['logado']
#         if ('logado' not in session):
#             # Retorna para a URL de login caso o usuário não esteja logado
#             return redirect(url_for('index'))

#         return f(*args, **kwargs)
#     return funcao_decorada