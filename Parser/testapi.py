import requests

items = []
with open("xml_data.txt", 'r') as f:
    items = f.readlines()

for each in items:
    r = requests.get(url = 'http://localhost:5000/parse?', params = {"data": each})
    print r.content
