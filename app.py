# -*- coding: utf-8 -*-
"""flask.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iAyiAvlGVEHp_z9Hxbyxm-0LG4GwUSpc"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import re
import string
from flask import Flask,jsonify,request
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost
import pickle
from flask_cors import CORS
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

df = pd.read_csv("contoh.csv")
df2 = pd.DataFrame()
df2['title'] = ['Malaysia Sudutkan RI: Isu Kabut Asap hingga Invasi Babi']

def text_preproc(x):
  #case folding
  x = x.lower()
  #remove double space
  x = re.sub(r'\s{2,}', ' ', x)
  return x

df2['Judul Berita (Bersih)'] = df2['title'].apply(text_preproc)
df.head()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = TfidfVectorizer(binary=True)
#X_train_vec = vectorizer.fit_transform(X_train).toarray()
#X_test_vec = vectorizer.fit_transform(X_test).toarray()

tfidfvoc = vectorizer.fit(df2['Judul Berita (Bersih)'])
tfidfvec = vectorizer.fit_transform(df2['Judul Berita (Bersih)']).toarray()

print(tfidfvec.shape)

#load vectorizer.vocabulary_
kosaKata = pickle.load(open("feature.pkl", "rb"))

#load vectorizer.vocabulary_
xgb_model_loaded = pickle.load(open("xgbmodel.sav", "rb"))

vectorizer.fit(kosaKata)

print(tfidfvoc.vocabulary_)

transform = vectorizer.transform(df2['Judul Berita (Bersih)']).toarray()

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

# make predictions for test data
predict = xgb_model_loaded.predict(transform)
predictions = [round(value) for value in predict]
print(predict)

from flask_cors import CORS
from flask_ngrok import run_with_ngrok
from flask import Flask,jsonify,request

app = Flask(__name__)
if name == 'main':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
@app.route("/")
def home():
    return "<h1>Running Flask on Google Colab!</h1>"

@app.route('/api/sentence', methods=["GET"])
def sentece():
    arr_text = []
    text = request.args.get("text")
    arr_text.append(text) 
    clean_arr_text = list(map(text_preproc,arr_text))
    x_sentence = vectorizer.transform(clean_arr_text)
    predict = xgb_loaded_model.predict(x_sentence)
    resp = jsonify({"text":text,"prediction":int(predict[0])})
    return resp

@app.route('/api/file', methods=["POST"])
def byFile():
    request_data = request.get_json()
    data_komentar = request_data['data']

    arr_text = []

    for f in data_komentar :
      arr_text.append(f)

    clean_arr_text = list(map(text_preproc,arr_text))
    x_sentence = vectorizer.transform(clean_arr_text)
    predict = loaded_model.predict(x_sentence)

    kalimats = []
    prediksis = []
    # resp['kalimats'] = [None]
    # resp['prediksis'] = [None]
    for count,f in enumerate(predict) :
      kalimat = arr_text[count],
      prediksi = int(f)
      kalimats.append(kalimat)
      prediksis.append(prediksi)
      # resp['kalimats'].append(kalimat)
      # resp['prediksis'].append(prediksi)

    return jsonify({"text":kalimats,"predictions":prediksis})

@app.route('/api/testjson', methods=["POST"])
def postJsonHandler():
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted'

app.run()