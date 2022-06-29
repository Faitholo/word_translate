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

# Handle session timeouts
s = requests.Session()
s.mount('https://api.cognitive.microsofttranslator.com', HTTPAdapter(max_retries=5))

from dotenv import load_dotenv
load_dotenv('/home/faith/word_translate/.env')


app = Flask(__name__)

app_id  = os.environ.get('ID')
app_key  = os.environ.get('API_KEY2')
app.secret_key = os.environ.get('SECRET_KEY')
db_password = os.environ.get("DB_PASSWORD")

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Quiz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hwbjpptpnxwont:7f3e5cf5a00cfb46e8981216b324317d205d88cd08ec514fe90b6126b38a5206@ec2-23-23-151-191.compute-1.amazonaws.com:5432/d9gk850om0pqfj'
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
# Paginate db query results
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
    # Return homepage
    return render_template('index.html')


@app.route('/translate', methods=['GET'])
def index():
    # Return translation page
    return render_template('translate.html')


@app.route('/translate', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'result.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )


@app.route('/dictionary')
def get_word():
    return render_template('dict.html')

@app.route('/dictionary', methods=['POST'])
def define_word():
    word = request.form['text']
    url1 = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{}?fields=definitions&strictMatch=false".format(word)
    url2 = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{}?fields=examples&strictMatch=false".format(word)
    url3 = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{}?fields=domains&strictMatch=false".format(word)
    url4 = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/{}?fields=pronunciations&strictMatch=false".format(word)
    
    
    r = requests.get(url1, headers = {"app_id": app_id, "app_key": app_key})
    r2 = requests.get(url2, headers = {"app_id": app_id, "app_key": app_key})
    r3 = requests.get(url3, headers = {"app_id": app_id, "app_key": app_key})
    r4 = requests.get(url4, headers = {"app_id": app_id, "app_key": app_key})
    
    
    results = r.json()
    results2 = r2.json()
    results3 = r3.json()
    results4 = r4.json()
    
    
    data = []
    data_input = {}
    not_found = "Word not found"
    
    try:
        defn = results["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        name = results3["id"]
        example1 = results2["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
        lang = results["results"][0]["language"]
        lex = results3["results"][0]["lexicalEntries"][0]["lexicalCategory"]["text"]
        pron = results4["results"][0]["lexicalEntries"][0]["entries"][0]["pronunciations"][0]["audioFile"]
        
        data_input.update({'defn': defn,
                           'word': name,
                           'example': example1,
                           'lang': lang,
                           'lex': lex})
    except IndexError:
        return (not_found)
    
    except KeyError:
        return(not_found)
    finally:
        data.append(data_input)
    
    return render_template('dict_result.html', data=data, pron=pron)



@app.route('/create', methods=['GET'])
def create_quiz():
    # Get the form for adding quiz questions
  form = Question()
  return render_template('questions.html', form=form)

@app.route('/create', methods=['POST'])
def create_quiz_submission():
  
  # Request data from the Question Form
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
def get_quiz():
    # Query the database to get all quiz questions
    all = Quiz.query.all()
    
    quiz = all
    
    return render_template('quiz.html', quiz=quiz)


@app.route('/quiz', methods=['POST'])
def play_quiz():
    # Query the database to get all quiz questions
    all = Quiz.query.all()
    
    quiz = all
    
    return render_template('answer.html', quiz=quiz)



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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
