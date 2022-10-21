from flask import Blueprint
from flask_restful import Api, Resource
from flask import request
from agropec.model.Bovine import Bovine

from agropec.model.Earring import Earring
from playhouse.shortcuts import model_to_dict, dict_to_model

bp = Blueprint("api", __name__)
api = Api(bp)

class HelloWorld(Resource):
    def post(self):
        json = request.get_json()
        
        earring = Earring.create(
            value = json.get('earring').get('value'),
            color = json.get('earring').get('color'),
        )
        
        bv = Bovine.create(
            sex = json.get('sex'),
            category = json.get('category'),
            weight = json.get('weight'),
            earring = earring,
        )
        
        print(str(bv))
        
        return model_to_dict(bv)
    
    def get(self):
        result = []
        rows=Bovine.select()
        for row in rows:
            result.append(model_to_dict(row))
            
        return result         
    
class Ping(Resource):
    def get(self):
        return None, 204

api.add_resource(HelloWorld, '/')
api.add_resource(Ping, '/ping')

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def init_app(app):
    Earring.create_table()
    Bovine.create_table()
    app.register_blueprint(bp)
    app.after_request(after_request)