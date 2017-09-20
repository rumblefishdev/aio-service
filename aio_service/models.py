import peewee as pw

from .db import database_proxy


class BaseModel(pw.Model):
    class Meta:
        database = database_proxy
