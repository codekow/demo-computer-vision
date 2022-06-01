#!/usr/bin/env python3.8
from flask import Flask
from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from waitress import serve, logging

from functions.capture_functions import *

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

class Test(Resource):
    def get(self):
        x = test()
        return jsonify(x)

class Capture(Resource):
    def get(self):
        x = capture()
        return jsonify(x)

api.add_resource(Test,'/test')
api.add_resource(Capture,'/capture')

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(app, host='0.0.0.0', port=5000)
