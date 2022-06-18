from distutils.debug import DEBUG
import json
from flask import Flask, render_template, url_for, jsonify, request
import requests, uuid
from flask_wtf import Form
from forms import *
import os
import urllib.request, json
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount('https://api.cognitive.microsofttranslator.com', HTTPAdapter(max_retries=5))

from dotenv import load_dotenv
load_dotenv('/home/faith/dictionary_api/.env')


app = Flask(__name__)

app_id  = os.environ.get('ID')
app_key  = os.environ.get('API_KEY2')
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def home():
    url = "https://od-api.oxforddictionaries.com/api/v2/translations/en/id/father?strictMatch=false"
    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    
    return render_template('index.html')


@app.route('/translate', methods=['GET'])
def get_word():
    form = Language()
    return render_template('translate.html', form=form)


@app.route('/translate', methods=['POST'])
def translate_word():
    key = os.environ.get('key_var_name')
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = os.environ.get('region_var_name')
    path = '/translate'
    constructed_url = endpoint + path

    form = Language()
    to = form.translate.data
    speech = form.lang.data
    
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': to
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': speech
    }]


    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    get_data = json.dumps(response, sort_keys=True, skipkeys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    data_response = json.loads(get_data)
    
    data = []
    for item in data_response:
        for each in item:
            data1 = item[each]
            for data2 in data1:
                data3 = data2
                
                for each_item in data3:
                    data.append(data3[each_item])

    
    return render_template('result.html', result=data, form=form)


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "Resource not found"}),
        404,
    )

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Unprocessable"}),
        422,
    )

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

@app.errorhandler(405)
def not_found(error):
    return (
        jsonify({"success": False, "error": 405, "message": "Method not allowed"}),
        405,
    )

if __name__ == '__main__':
    app.run(debug=True)
