from peewee import *

from miskatonic.config import Config


class Category(Model):
    title = CharField()

    class Meta:
        database = Config.db
