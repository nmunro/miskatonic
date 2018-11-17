from typing import List
import datetime

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
        self.slug = self.title.replace(' ', '_').lower()
        super().save()
