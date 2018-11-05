from peewee import *

from miskatonic.config import Config


class Tag(Model):
    title = CharField()

    class Meta:
        database = Config.db
