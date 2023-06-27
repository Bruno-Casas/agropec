"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

from agropec.model.Bovine import Bovine
from agropec.model.Category import Category
from agropec.model.Color import Color
from agropec.model.Earring import Earring
from peewee_migrate import Migrator
from decimal import ROUND_HALF_EVEN


def migrate(migrator: Migrator, database, fake=False, **kwargs):
    migrator.create_model(Category)
    migrator.create_model(Color)
    migrator.create_model(Earring)
    migrator.create_model(Bovine)


def rollback(migrator: Migrator, database, fake=False, **kwargs):
    migrator.remove_model(Category, cascade=True)
    migrator.remove_model(Color, cascade=True)
    migrator.remove_model(Earring, cascade=True)
    migrator.remove_model(Bovine, cascade=True)
