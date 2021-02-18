import mariadb
from dotenv import load_dotenv, find_dotenv
import os
from typing import Any
from functools import wraps
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')
SECRET_KEY = str(os.environ.get('SECRET_KEY'))
PROJECT_NAME = str(os.environ.get('PROJECT_NAME'))
DEBUG = str(os.environ.get('DEBUG'))


class Database:
    def __init__(self, name, database=None):
        try:
            if name == 'database':
                self._conn = mariadb.connect(
                    user=os.environ.get('MARIADB_USER'),
                    password=os.environ.get('MARIADB_PASS'),
                    host=os.environ.get('MARIADB_HOST'),
                    database=os.environ.get('MARIADB_DB'),
                )
                self._cursor = self._conn.cursor()
            else:
                raise()
        except:
            print('\n\nErro de conexão com o DB, verifique a classe e as variáveis de conexão!!!\n\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]

    def query_array(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()
        
    def query_dict(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.dictfetchall()


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