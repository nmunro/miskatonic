import os

from peewee import SqliteDatabase


class Config:
    db = SqliteDatabase(f'{os.getenv("MISKATONIC_DB")}.db')
