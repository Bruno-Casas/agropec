from peewee import *
from .Base import BaseModel
from .Earring import Earring

class Bovine(BaseModel):
    id = BigAutoField()
    sex = SmallIntegerField()
    category = SmallIntegerField()
    weight = FloatField()
    earring = ForeignKeyField(Earring, backref='tweets')
