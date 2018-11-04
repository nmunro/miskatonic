import os

from playhouse.db_url import connect


class Config:
    db = connect(os.getenv('DATABASE_URL'))
    SECRET_KEY = os.getenv('SECRET_KEY')
