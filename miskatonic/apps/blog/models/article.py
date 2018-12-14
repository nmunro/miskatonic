from typing import List
import datetime
import string

from peewee import Model, CharField, TextField, DateTimeField

from miskatonic.config import Config


class Article(Model):
    title = CharField()
    slug = CharField()
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = Config.db

    def save(self, force_insert: bool = False, only: List = None):
        fn = lambda c: c.lower() if c.lower() in [*string.ascii_lowercase, *string.digits] else '_'
        self.slug = ''.join(map(fn, self.title)).lower()
        super().save()
