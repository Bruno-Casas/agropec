from peewee import *
from .Base import BaseModel

class Color(BaseModel):
    id = AutoField()
    alias = CharField(max_length=32, unique=True)
    code = IntegerField(null=True, unique=True)
    