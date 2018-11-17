from flask_login import UserMixin
from peewee import Model, CharField
from werkzeug.security import generate_password_hash, check_password_hash

from miskatonic.config import Config


class Person(UserMixin, Model):
    username = CharField()
    email = CharField()
    password_hash = CharField()

    class Meta:
        database = Config.db

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)
