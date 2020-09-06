import re
import json
from collections import Counter
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER


def remove_punctuation(line):
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
    return line

def processing_pos(original_sentence:str, seg_list: list, pos_list: list, need_pos: list):
    print('Starting clean no need Part of Speech...')
    output = {}
    for seg, pos in zip(seg_list, pos_list):
        if pos in need_pos:
            positions = segment_postitions(original_sentence, seg)
            output[seg] = {
                'Title': seg,
                'POS': pos,
                'Absolute_positions': positions,
                'Frequency': len(positions)
            }
            # output.append([pos, seg_list.count(seg), seg, positions])
    return output

def segment_postitions(text: str, word: str):
    positions = []
    for m in re.finditer(word, text):
        positions.append([m.start(), m.end()])
    return positions

def processing_ner(original_sentence:str, entitys: set):
    output = {}

    for entity in entitys:
        title, pos = entity[-1], entity[-2]
        title = remove_punctuation(title)
        positions = segment_postitions(original_sentence, title)
        output[title] = {
                'Title': title,
                'POS': pos,
                'Absolute_positions': positions,
                'Frequency': len(positions)
            }
    return output


def integrate_pos_ner(processed_pos: dict, ner: set):
    # replace the POS with NER
    for entity in ner:
        if entity in processed_pos:
            processed_pos[entity]['POS'] = entity[-2]


def pos2json(original_sentence, word_list, pos_list, entity_list):
    data = {'original_input':original_sentence ,'tokenize_output':[], 'NER_output':[]}

    for word, pos in zip(original_sentence, pos_list):
        if pos in ['Na', 'Nb', 'Nc']:
            start_idx = original_sentence.find(word)
            end_idx = start_idx + len(word) - 1 

            data['tokenize_output'].append({
                'title' : word,
                'part_of_speech' : pos,
                'absolute_position' : [[start_idx, end_idx]],
                'frequency' : 1})

    for entity in entity_list:
        start_idx, end_idx = entity[0], entity[1]
        ner = entity[2]
        word = entity[3]

        data['NER_output'].append({
            'title' : word,
            'part_of_speech' : ner,
            'absolute_position' : [[start_idx, end_idx]],
            'frequency' : 1})
    return data

def load_models(model_path):
    ws = WS(model_path)
    pos = POS(model_path)
    ner = NER(model_path)
    return ws, pos, ner

# if __name__ == '__main__':
#     ws = WS("../data")
#     pos = POS("../data")
#     ner = NER("../data")
#     need_pos = ['Na', 'Nb', 'Nc']

#     with open('../test_data.json') as json_file:
#         datas = json.load(json_file)
    
#     sentence_list = []
#     for data in datas:
#         sentence_list.append(data['content'])

#     # sample text
#     # sentence_list = [   
#     # "傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。",
#     # "美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。",
#     # "",
#     # "土地公有政策?？還是土地婆有政策。.",
#     # "… 你確定嗎… 不要再騙了……",
#     # "最多容納59,000個人,或5.9萬 人,再多就不行了.這是環評的結論.",
#     # "科長說:1,坪數對人數為1:3。2,可以再增加。",
#     # ]
#     # sentence_list = ["很多經歷了戰爭、捱餓、流行病等苦難的人，在餘生中會活得更加健康和長壽。一方面，長壽可能是基因決定的，但在更大程度上，長壽是由一個人的品質或心態決定的。長壽的人有高度的自覺性，有更強的責任心，不會進行「向上比較」，而是追求自身生活的意義和內心的富足。"]
#     # sentence_list = ["傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。"]
#     # sentence_list = ["美國擴大對華為技術封鎖，台積電也決定延後五奈米擴建及三奈米試產，延後時間長達二季，順延至明年第一季，將待美中貿易戰明朗化後再做定奪。供應鏈透露，台積電上周緊急通知設備商，原訂自七月起到今年底交貨的設備，全暫停交貨。台積電坦承美方五月十五日頒布新出口禁令，二周的申訴期極為關鍵，若變數未釐清，台積電就會被迫調整，但尚無下修全年資本支出打算。台積電稍早公布今年資本支出一百五十億美元至一百六十億美元，其中約百分之八十將用於三奈米、五奈米與七奈米等先進製程技術。台積電捲入美中科技戰，美國商務部頒布新出口禁令後，對台積電帶來極大限制。台積電為突破美方新出口限制傷害，近期也擴大在美國負責政府關係部門編制，極力與華府溝通。另一方面也停接華為旗下海思新單，避免在未找到突破點前觸犯美國法規，但海思在五月十五日下的五奈米及十二奈米大單，台積電已透過增產方式，趕在一百二十天寬限期交貨。據了解，台積電為海思提供每月二萬多片五奈米產能，五月起拉升至每天一千片，增幅逾四成，換算每月產能推升近三萬片，已超過蘋果的二點七萬片，台積電為蘋果備買的產能下月仍預定將拉升至三萬片，將與海思相近。不過，由於一百二十天寬限期截止後，台積電即不再承接海思新單，因此原本預定打算在十八廠第三期（P3）擴增近三萬片的的五奈米強化版計畫，決定延後二季，預定順延至明年第一季。至於三奈米試產線，原預定今年六月裝設，也同步順延至明年第一季。但台積電內部透露，二奈米研發仍不會受華為新出口禁令影響，仍加速進行中。台積電表示不會透露個別客戶產能配置，至於三奈米試產時間，將於法說會對外說明。"]

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

#         datas[idx]['POS'] = pos_output
#         datas[idx]['NER'] = ner_output
#         datas[idx]['Final'] = final_output
    
#     with open('./testoutput.json', 'w') as json_file:
#         json.dump(datas, json_file, ensure_ascii=False, indent=4)
    
#     # with open('pos.json', 'w') as f:
#     #     json.dump(pos_out_list, f, ensure_ascii=False)
#     # with open('ner.json', 'w') as f:
#     #     json.dump(ner_out_list, f, ensure_ascii=False)
#     # with open('final.json', 'w') as f:
#     #     json.dump(final_out_list, f, ensure_ascii=False)
#     #print(json.dumps(final_output, indent=2, ensure_ascii=False))

