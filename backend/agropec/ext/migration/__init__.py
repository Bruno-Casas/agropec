import click

from flask.cli import with_appcontext
from peewee_migrate import Router
from agropec.ext.database import db

router = Router(db)

@click.group()
@with_appcontext
def migration():
    pass


@migration.command('create')
@click.argument('name')
def migration_create(name):
    if not name:        
        raise Exception('O nome da migração é obrigatório')
    
    router.create(name)


@migration.command('run')
def migration_run():
    router.run()

@migration.command('rollback')
def migration_rollback():
    router.rollback()

def init_app(app):
    app.cli.add_command(migration)
    