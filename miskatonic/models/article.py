import datetime

from peewee import *

from miskatonic.config import Config

from .category import Category


class Article(Model):
    title = CharField()
    slug = CharField()
    category_id = ForeignKeyField(Category, backref='articles')
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = Config.db

    def save(self, force_insert: bool = False, only = None):
        self.slug = self.title.replace(' ', '_').lower()
        super().save()
