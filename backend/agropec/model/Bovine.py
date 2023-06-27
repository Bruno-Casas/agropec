from peewee import *

from .Category import Category
from .Base import BaseModel
from .Earring import Earring

class Bovine(BaseModel):
    id = AutoField()
    sex = SmallIntegerField()
    weight = FloatField()
    category = ForeignKeyField(Category, backref='id')
    earring = ForeignKeyField(Earring, backref='id')

