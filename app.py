from distutils.debug import DEBUG
import json
from flask import Flask, render_template, url_for, jsonify, request, flash, abort
import requests, uuid
from flask_wtf import Form
from forms import *
import os
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import urllib.request, json
from requests.adapters import HTTPAdapter
from models import db, Quiz

#s = requests.Session()
#s.mount('https://api.cognitive.microsofttranslator.com', HTTPAdapter(max_retries=5))

from dotenv import load_dotenv
load_dotenv('/home/faith/dictionary_api/.env')


app = Flask(__name__)

app_id  = os.environ.get('ID')
app_key  = os.environ.get('API_KEY2')
app.secret_key = os.environ.get('SECRET_KEY')
db_password = os.environ.get("DB_PASSWORD")

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Quiz'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response

"""
QUESTIONS_PER_PAGE = 1


def paginate(request, data):
    #Pagination function limiting to 1 question per page
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_data = [item.format() for item in data]

    return formatted_data[start: end]
"""




@app.route('/')
def home():
    
    return render_template('index.html')


@app.route('/translate', methods=['GET'])
def get_word():
    form = Language()
    return render_template('translate.html', form=form)


@app.route('/translate', methods=['GET','POST'])
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



@app.route('/create', methods=['GET'])
def create_quiz():
  form = Question()
  return render_template('questions.html', form=form)

@app.route('/create', methods=['POST'])
def create_quiz_submission():
  
  # Request data from the Venue Form
  if request.method == "POST":
    form = Question()
    quiz = Quiz(question = form.question.data,
                A = form.A.data,
                B = form.B.data,
                C = form.C.data,
                D = form.D.data,
                answer = form.answer.data
                )
    # Add and commit the received form input
    db.session.add(quiz)
    db.session.commit()
    flash('Question: ' + request.form['question'] + ' was successfully listed!')

    db.session.close()
  else:
    flash('An error occurred. Question: ' + request.form['question'] + ' could not be listed!')
    db.session.rollback()
  
  return render_template('questions.html', form=form)

 

@app.route('/quiz', methods=['GET'])
def play_quiz():
    form = Question()
    all = Quiz.query.all()
    
    quiz = all
    
    return render_template('quiz.html', form=form, quiz=quiz)



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
