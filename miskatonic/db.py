import datetime
import os

from peewee import *


db = SqliteDatabase('articles2.db')


def create_tables():
    with db:
        db.create_tables([Category, Article])


class Category(Model):
    title = CharField()

    class Meta:
        database = db


class Article(Model):
    title = CharField()
    slug = CharField()
    category = ForeignKeyField(Category, backref='articles')
    content = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def save(self, force_insert: bool = False, only = None):
        self.slug = self.title.replace(' ', '_').lower()
        super().save()
