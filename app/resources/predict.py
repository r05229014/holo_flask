import os
import re
import json
import numpy as np
import requests
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask import current_app as app
from .utils import (
    remove_punctuation, processing_pos, segment_postitions,
    processing_ner, integrate_pos_ner, pos2json, load_models)


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
