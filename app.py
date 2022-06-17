from distutils.debug import DEBUG
import json
from flask import Flask, render_template, url_for, jsonify, request
import requests, uuid
from flask_wtf import Form
from forms import *
import os

import urllib.request, json

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

"""
@app.route('/word', methods=['GET'])
def get_word():
    form = Language()
    return render_template('list.html', form=form)
    
    #url = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/father?fields=etymologies&strictMatch=false"
    #r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    
    #d_text = r.json()
    
    #abc = d_text["results"]
    #data = []
    #for i in abc:
        #data.append(i)
    
    #return render_template('list.html', data=data)
    
    
    #j_form = json.dumps(r.json())
    
    #print("code {}\n".format(r.status_code))
    #print("text \n" + r.text)
    #print("json \n" + json.dumps(r.json()))
    
    
    
    #return d_text

    
@app.route('/word', methods=['POST'])
def def_word():
    form = Language()
    data = form.lang.data
    trans = form.translate.data
    url = "https://od-api.oxforddictionaries.com/api/v2/translations/en/{}/{}?strictMatch=false".format(trans, data)
    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    
    
    d_text = r.json()
    return d_text
"""


@app.route('/azure', methods=['GET'])
def azure_word():
    form = Language()
    return render_template('azure.html', form=form)

@app.route('/azure', methods=['POST'])
def azure_translate():
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

    # You can pass more than one object in body.
    body = [{
        'text': speech
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    dat = json.dumps(response, sort_keys=True, skipkeys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    datt = json.loads(dat)
    
    data = []
    for i in datt:
        for a in i:
            dattt = i[a]
            for o in dattt:
                data1 = o
                
                for r in data1:
                    data.append(data1[r])

    
    return render_template('azure.html', result=data, form=form)


if __name__ == '__main__':
    app.run(debug=True)
