import os
from flask import Flask
from agropec.ext import configuration

def minimal_app():
    app = Flask(__name__)
    configuration.init_app(app)
    return app

def create_app():
    app = minimal_app()
    configuration.load_extensions(app)
    return app


print(os.getcwd())