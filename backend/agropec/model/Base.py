from peewee import *
from agropec.ext.database import db

# Create a base-class all our models will inherit, which defines
# the database we'll be using.
class BaseModel(Model):
    class Meta:
        database = db