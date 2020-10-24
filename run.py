from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from app.resources.predict import Predict
from flask_celery import make_celery


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['CELERY_BROKE_URL'] = 'localhost'
    api = Api(app)
    api.add_resource(Predict, '/predict')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True) 

