import os
import re
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_restful import Resource
from flask import current_app as app
from .utils import (
    remove_punctuation, processing_pos, segment_postitions,
    processing_ner, integrate_pos_ner, pos2json, load_models)


# @app.route('/predict', methods = ['POST'])
# def Predict():
#     if request.is_json:
#         contents = request.get_json()
#     if contents is not None:
#         print('Loading model...')
#         ws, pos, ner = load_models(app.config['MODEL_PATH'])
    
#     # start to processing
#     sentence_list = []
#     for data in contents:
#         sentence_list.append(data['content'])
    
#     word_sentence_list = ws(sentence_list,
#                             sentence_segmentation = True,  # To consider delimiters
#                             segment_delimiter_set = {",", "，", "。", ":", "?", "!", ";",
#                                                      "(", ")", "（", "）",
#                                                      ".", "%", "、", "·", "《", "》",
#                                                      "「", "」", "：", "#", ""})
#     pos_sentence_list = pos(word_sentence_list)
#     entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

#     for idx, (sentence, word, pos, entity) in enumerate(zip(sentence_list, word_sentence_list, pos_sentence_list, entity_sentence_list)):
#         pos_output = processing_pos(sentence, word, pos, need_pos)
#         ner_output = processing_ner(sentence, entity)
#         final_output = dict(pos_output, **ner_output)

#         contents[idx]['POS'] = pos_output
#         contents[idx]['NER'] = ner_output
#         contents[idx]['Final'] = final_output
#     print(contents[0])
#     return jsonify(contents)

class Predict(Resource):
    def post(self):
        if request.is_json:
            contents = request.get_json()
        if contents is not None:
            print('Loading model...')
            ws, pos, ner = load_models(app.config['MODEL_PATH'])
            need_pos = ['Na', 'Nb', 'Nc']
        
        # start to processing
        sentence_list = []
        for data in contents:
            sentence_list.append(data['content'])
        
        word_sentence_list = ws(sentence_list,
                                sentence_segmentation = True,  # To consider delimiters
                                segment_delimiter_set = {",", "，", "。", ":", "?", "!", ";",
                                                        "(", ")", "（", "）",
                                                        ".", "%", "、", "·", "《", "》",
                                                        "「", "」", "：", "#", ""})
        pos_sentence_list = pos(word_sentence_list)
        entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

        for idx, (sentence, word, pos, entity) in enumerate(zip(sentence_list, word_sentence_list, pos_sentence_list, entity_sentence_list)):
            pos_output = processing_pos(sentence, word, pos, need_pos)
            ner_output = processing_ner(sentence, entity)
            final_output = dict(pos_output, **ner_output)

            contents[idx]['POS'] = pos_output
            contents[idx]['NER'] = ner_output
            contents[idx]['Final'] = final_output
        return jsonify(contents)
