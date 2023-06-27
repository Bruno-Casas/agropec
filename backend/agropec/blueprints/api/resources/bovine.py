

import json
from flask import request
from flask_restful import Resource

from agropec.model.Color import Color
from agropec.model.Bovine import Bovine
from agropec.model.Earring import Earring

from playhouse.shortcuts import model_to_dict

from agropec.blueprints.api import rest_api
from agropec.model.Category import Category
from peewee import *

class BovineResource(Resource):
    def post(self):
        collections = request.get_json()
        
        resp = []
        
        print(collections)
        for collection in collections:
            packages = collection.get('packages')
            for package in packages:
                bv = json.loads(package)
                print('!!!!!!!!!!!!!!', bv)
                
                category = Category.get_or_none(Category.name == bv.get('category').get('name')) 
                if not category:
                    category = Category.create(
                        id = None,
                        name = bv.get('category').get('name')
                    )
                
                color = Color.get_or_none(Color.alias == bv.get('earring').get('color').get('alias')) 
                if not color:
                    color = Color.create(
                        id = None,
                        alias = bv.get('earring').get('color').get('alias'),
                        code = bv.get('earring').get('color').get('code')
                    )
            
                earring = (Earring
                    .select()
                    .where(Earring.number == bv.get('earring').get('number') or Earring.code == bv.get('earring').get('code'))
                    .get_or_none())
                
                if not earring:
                    earring = Earring.create(
                        id = None,
                        code = bv.get('earring').get('code'),
                        number = bv.get('earring').get('number'),
                        color = color
                    )
                    
                bv = Bovine.create(
                    id = None,
                    sex = bv.get('sex'),
                    weight = bv.get('weight'),
                    category = category,
                    earring = earring
                )
                
                resp.append(self._get_dict(bv))
                
        pass

        return resp
    
    def get(self):
        result = []
        rows = Bovine.select()
        
        for model in rows:
            result.append(self._get_dict(model))
            
        return result
    
    def _get_dict(self, model):
            model_dict = {'id': model.__dict__.get('id'), **model.__data__}
            for field in model._meta.sorted_fields:
                if not isinstance(field, ForeignKeyField):
                    continue
                
                field_value = getattr(model, field.name)
                
                if issubclass(type(field_value), Model):
                    model_dict[field.name] = self._get_dict(field_value)
                else:
                    model_dict[field.name] = self._get_dict(field.rel_model.get_by_id(field_value))
                 
                
            return model_dict
    
rest_api.add_resource(BovineResource, '/bovine')
