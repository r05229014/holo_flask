import requests
import json

BASE = 'http://35.221.178.255:8080/'
url = BASE + 'predict/post'


with open('app/test_data/test_data.json') as json_file:
        data = json.load(json_file)
r = requests.post(BASE + '/predict', json=data)
print(r)
