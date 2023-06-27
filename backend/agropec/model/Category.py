from peewee import *

from agropec.model.Base import BaseModel

class Category(BaseModel):
    id = AutoField()
    name = CharField(max_length=32)
    