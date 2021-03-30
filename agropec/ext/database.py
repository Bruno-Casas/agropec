from flask import g
from flask_peewee.db import Database, DatabaseProxy, Proxy

db = DatabaseProxy()

def init_app(app):
    database = Database(app)
    db.initialize(database)