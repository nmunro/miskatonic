import datetime
import os

from peewee import *

from miskatonic.config import Config

config = Config()


def create_tables():
    with config.db:
        config.db.create_tables([Category, Article])


class Category(Model):
    title = CharField()

    class Meta:
        database = config.db


class Article(Model):
    title = CharField()
    slug = CharField()
    category = ForeignKeyField(Category, backref='articles')
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = config.db

    def save(self, force_insert: bool = False, only = None):
        self.slug = self.title.replace(' ', '_').lower()
        super().save()
