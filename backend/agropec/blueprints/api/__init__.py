from agropec.model.Color import Color
from flask import Blueprint
from flask_restful import Api, Resource
from flask import request
from agropec.model.Bovine import Bovine

from agropec.model.Earring import Earring
#from agropec.blueprints.api.resources.bovine import BovineResource

module_blueprint = Blueprint("api", __name__)
rest_api = Api(module_blueprint, '/api/rest')         
    
class _PingResource(Resource):
    def get(self):
        return None, 204

#api.add_resource(HelloWorld, '/')
rest_api.add_resource(_PingResource, '/ping')

from os.path import dirname, basename, isfile, join
import glob

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def init_app(app):
    resources_path = 'agropec.blueprints.api.resources'
    resources_names = glob.glob(join(dirname(__file__), "resources/*.py"))
    
    for resource in resources_names:
        if isfile(resource) and not resource.endswith('__init__.py'):
            __import__(f'{resources_path}.{basename(resource)[:-3]}')
            
        pass
    
    app.register_blueprint(module_blueprint)
    app.after_request(after_request)
