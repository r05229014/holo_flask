import os
import re
import json
import numpy as np
import requests

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
# from app.resources.predict import Predict
from flask_celery import make_celery
from flask import current_app as app
from celery import Celery
from app.resources.utils import (
    remove_punctuation, processing_pos, segment_postitions,
    processing_ner, integrate_pos_ner, pos2json, load_models)



celery = Celery('tasks', broker='redis://localhost:6379')


class Predict(Resource):
    def __init__(self):
        self.ws, self.pos, self.ner = load_models(app.config['MODEL_PATH'])
        self.need_pos = ['Na', 'Nb', 'Nc']
        
    def get(self):
        return 'testhaha'

    @celery.task()
    def post(self):
        if request.is_json:
            contents = request.get_json()
        
        # start to processing
        sentence_list = []
        for data in contents:
            sentence_list.append(data['content'])
        
        word_sentence_list = self.ws(sentence_list,
                                sentence_segmentation = True,  # To consider delimiters
                                segment_delimiter_set = {",", "，", "。", ":", "?", "!", ";",
                                                        "(", ")", "（", "）",
                                                        ".", "%", "、", "·", "《", "》",
                                                        "「", "」", "：", "#", ""})
        pos_sentence_list = self.pos(word_sentence_list)
        entity_sentence_list = self.ner(word_sentence_list, pos_sentence_list)

        for idx, (sentence, word, pos, entity) in enumerate(zip(sentence_list, word_sentence_list, pos_sentence_list, entity_sentence_list)):
            pos_output = processing_pos(sentence, word, pos, self.need_pos)
            ner_output = processing_ner(sentence, entity)
            final_output = dict(pos_output, **ner_output)

            contents[idx]['POS'] = pos_output
            contents[idx]['NER'] = ner_output
            contents[idx]['Final'] = final_output

        return jsonify(contents)



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

