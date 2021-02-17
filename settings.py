from fastapi import FastAPI
import mariadb
from dotenv import load_dotenv, find_dotenv
import os

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



# with Database('database') as db:
#     res = db.query_dict('SELECT top 1 * FROM database')
#     print(res[0]['DT_INGRESSO'])

