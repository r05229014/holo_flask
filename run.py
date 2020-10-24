from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from app.resources.predict import Predict
from flask_celery import make_celery
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:7777')



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379'
    )
    celery = make_celery(app)
    api = Api(app)
    api.add_resource(Predict, '/predict')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True) 

