from flask_peewee.db import DatabaseProxy
from peewee import *

db = DatabaseProxy()

def init_app(app):
    config = app.config.get('DATABASE')
    
    database = PostgresqlDatabase(
        config.get('db'),
        user=config.get('user'),
        password=config.get('password'),
        host=config.get('host')
        )
    
    database = database
    db.initialize(database)