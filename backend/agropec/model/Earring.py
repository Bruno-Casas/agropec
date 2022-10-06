from peewee import *
from .Base import BaseModel

class Earring(BaseModel):
    id = BigAutoField()
    value = CharField()
    color = SmallIntegerField()