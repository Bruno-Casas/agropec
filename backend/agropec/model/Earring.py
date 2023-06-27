from peewee import *

from .Color import Color
from .Base import BaseModel

class Earring(BaseModel):
    id = PrimaryKeyField()
    number = IntegerField()
    code = TextField(unique=True)
    color = ForeignKeyField(Color, backref='id', lazy_load=False)