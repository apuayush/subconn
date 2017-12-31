from flask import Flask, request
from bs4 import BeautifulSoup as soup
import json

def parse(value):
    data = soup(value, "lxml").printletterbarcodedata
    res = {"name": data['name'], "uid": data['uid'], "district": data['dist'], "state": data['state'], "postalcode": data['pc'], "gender": data['gender']}
    return json.dumps(res)

app = Flask(__name__)

@app.route("/")
def api_home():
    return 'Aadhaar Parser Home'

@app.route("/parse")
def api_parse():
    if 'data' in request.args:
        return parse(request.args['data'])
    else:
        return 'Aadhaar Parser (No data)'

if __name__  == '__main__':
    app.run(debug=True)
