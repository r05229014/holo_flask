import os
from flask import Flask
from celery import Celery
from api.config import config


class Factory(object):
    def set_flask(self, **kwargs):
        """Flask instantiation."""
        # Flask instance creation
        self.flask = Flask(__name__, **kwargs)

        # Flask configuration
        self.flask.config.from_object(config[])

        # Swagger documentation
        self.flask.config.SWAGGER_UI_DOC_EXPANSION = 'list'
        self.flask.config.SWAGGER_UI_JSONEDITOR = True

        return self.flask

    def set_celery(self, **kwargs):
        """Celery instantiation."""
        # Celery instance creation
        self.celery = Celery(__name__, **kwargs)

        # Celery Configuration
        self.celery.conf.update(self.flask.config)

        return self.celery    