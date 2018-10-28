import os

from peewee import SqliteDatabase


class Config:
    def __init__(self):
        if os.getenv('DB_TYPE') == 'postgres':
            pass

        else:
            self.db = SqliteDatabase(f'{os.getenv("MISKATONIC_DB")}.db')
