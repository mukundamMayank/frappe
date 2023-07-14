import requests
import json


# title = None
# authors = None
json_data = {}

json_data['email'] = "mayank.7967@gmail.com"
json_data['title'] = "Mortals"


# response = requests.post('http://localhost:8000/storeBooks', json = json_data).content
# # response_json = json.loads(response)
# print(response)

response = requests.get('http://localhost:8000/getBooks?author=Rumi').content.decode('utf-8')

# response = requests.post('http://localhost:8000/returnBook', json=json_data).content
print(response)