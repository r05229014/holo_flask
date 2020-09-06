from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from app.resources.predict import Predict

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    api = Api(app)
    api.add_resource(Predict, '/predict')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000) 