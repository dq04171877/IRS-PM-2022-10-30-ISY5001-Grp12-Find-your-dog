#!/usr/bin/env python
# coding: utf-8

# ## **Import libraries**

import numpy as np
import pandas as pd
from pandas import DataFrame
import csv
import math
import heapq
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
import spacy
import en_core_web_sm
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin

from unicodedata import name
from flask import Blueprint, jsonify, request
import sqlite3
import sys
import json
from nlp_processor import *
from recommender_functions import *
from database_service import *


class Adopter:
    adopter_name = ''
    password = ''
    accomodation = -1  # -1: unknown, 1: hdb, 2: condo
    prefer_age_group = -1  # -1: unknown, 1: puppy, 10:middle, 100: old
    prefer_gender = -1  # -1: unknown, 1: male, 10: female
    personality_preference = ""  # TEXT description
    recommend_dog_index = ''  # [2,3,45]
    boring_tags = ''  # [0,0,0,0,0]


data = pd.read_csv('./newdata_2.csv')
shelter_adoption_data = pd.read_excel('./Shelter_Adoption_Data.xlsx')
database_path = './database.db'
schema_path = './schema.sql'

corpus = list(data['Corpus'])
# corpus_words = vectorizer.get_feature_names()
vectorizer1 = CountVectorizer()
word_vec = vectorizer1.fit_transform(corpus)
corpus_words = vectorizer1.get_feature_names()


nofilter = filter_dog(data, [0, 1], [0, 1, 2, 3], [0, 1])


con = sqlite3.connect(database_path)
with open(schema_path) as f:
    con.executescript(f.read())
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
cursor.close()
con.close()

api = Blueprint('api', __name__)


@api.route('/hello/<string:name>/')
@cross_origin()
def say_hello(name):
    response = {'msg': "Hello {}".format(name)}
    return jsonify(response)


@api.route('/recommend/signin', methods=['POST'])
@cross_origin(origin='*')
def signin():
    request_content = request.get_data()
    request_json = json.loads(request_content)
    print("request_json:", request_json)
    adopter_name = request_json['adopter_name']
    password = request_json['password']
    print("adopter_name:", adopter_name)
    if (is_adopter_in_db(adopter_name, password)):
        query_result = query_adopter_from_db(adopter_name)
        result_json = json.loads(query_result)
        user_info = {"adopter_name": result_json[0][1],
                     "password": result_json[0][2]}
        print("query data:", query_result)
        result = {'code': 'SU001', 'data': user_info}
        return jsonify(result)
    else:
        # The adopter does not exist, return
        result = {'code': 'ER001', 'msg': 'Invalid account or password!'}
        print(adopter_name, result)
        return jsonify(result)


@api.after_app_request
def after_app_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    print('add headers', response)

    return response


@api.route('/recommend/signup', methods=['POST'])
@cross_origin(origin='*')
def signup():
    request_content = request.get_data()
    request_json = json.loads(request_content)
    print("request_json:", request_json)
    adopter_name = request_json['adopter_name']
    password = request_json['password']
    accomodation = request_json['accomodation']
    prefer_age_group = str(request_json['prefer_age_group'])
    prefer_gender = str(request_json['prefer_gender'])
    personality_preference = request_json['personality_preference']
    elderly = int(request_json['Elderly']) if request_json['Elderly'] != '' else 1
    experience = int(request_json['experience']) if request_json['experience'] != '' else 1
    kid = int(request_json['kid']) if request_json['kid'] != '' else 1
    medical = int(request_json['medical']) if request_json['medical'] != '' else 1
    other_dog = int(request_json['other_dog']) if request_json['other_dog'] != '' else 1
    window = int(request_json['window']) if request_json['window'] != '' else 1
    boring_tags = [kid, elderly, other_dog, medical, experience, window]
    print("boring_tags", str(boring_tags))
    if (is_adopter_name_in_db(adopter_name)):
        # Dulplicate adopter name is not allowed
        print("in")
        result = {'code': 'ER002'}
        return jsonify(result)
    else:
        print('not in')
        adopter = Adopter()
        adopter.adopter_name = adopter_name
        adopter.password = password
        adopter.accomodation = accomodation
        adopter.prefer_age_group = prefer_age_group
        adopter.prefer_gender = prefer_gender
        adopter.personality_preference = personality_preference
        adopter.boring_tags = str(boring_tags)
        insert_adopter_to_db(adopter)
        response = jsonify({'code': 'SU002', "adopter_name": adopter_name, "password": password})
        print('response', response)
        return response


@api.route('/recommend/adopter_new_recommend', methods=['POST'])
@cross_origin()
def adopter_new_recommend():
    request_content = request.get_data()
    request_json = json.loads(request_content)
    print(request_json)
    adopter = Adopter()
    adopter.adopter_name = request_json['adopter_name']
    query_result = query_adopter_from_db(adopter.adopter_name)
    result_json = json.loads(query_result)
    # result_json[0][7]: dog_index
    print("result_json[0][8]:", result_json[0][8])
    boring_tags = list(map(int, json.loads(result_json[0][8])))
    print(type(boring_tags))
    if (result_json[0][7] == None):
        # result_json[0][5]:gender result_json[0][4]: age  result_json[0][3]:HDB result_json[0][6]:personality
        recommend_result = recommend_newuser(data, list(map(int, json.loads(result_json[0][5].replace("'", '"')))),
                                             list(map(int, json.loads(result_json[0][4].replace("'", '"')))),
                                             [int(result_json[0][3])], result_json[0][6],
                                             boring_tags, corpus, corpus_words, 5, filter_hard=True)
        adopter.recommend_dog_index = str(recommend_result)
        print("adopter.recommend_dog_index:", adopter.recommend_dog_index)
        result = update_recommend_dog_index_to_db(adopter)
        return get_adopter_new_recommend_response(recommend_result)
    else:
        result_list = json.loads(result_json[0][7])
        return get_adopter_new_recommend_response(result_list)


def get_adopter_new_recommend_response(recommend_result):
    response = {}
    for order, dog_index in enumerate(recommend_result):
        print("order:", order, "don_index:", dog_index)
        dog_pic_file = shelter_adoption_data.Picture_Folder_Name[dog_index]
        dog_link = shelter_adoption_data.Link[dog_index]
        dog_name = shelter_adoption_data.Name[dog_index]
        dog_gender = shelter_adoption_data.Gender[dog_index]
        dog_age = shelter_adoption_data.Age[dog_index]
        dog_home = shelter_adoption_data.HDB_Approved[dog_index]
        dog_organisation = shelter_adoption_data.Organisation[dog_index]
        dog_description = shelter_adoption_data.Personality[dog_index]
        response["dog_" + str(order)] = {"dog_pic_file": dog_pic_file + "/" + dog_pic_file + "1.jpg",
                                         "dog_link": dog_link,
                                         "dog_name": dog_name,
                                         "dog_gender": dog_gender,
                                         "dog_age": dog_age,
                                         "dog_home": dog_home,
                                         "dog_organisation": dog_organisation,
                                         "dog_description": dog_description,
                                         "dog_index": dog_index
                                         }
    print(response)
    return response


@api.route('/recommend/recommend_by_history', methods=['POST'])
@cross_origin()
def recommend_by_history():
    request_content = request.get_data()
    request_json = json.loads(request_content)
    print(request_json)
    adopter = Adopter()
    adopter.adopter_name = request_json['adopter_name']
    adopter.accomodation = request_json['accomodation']
    adopter.prefer_age_group = str(request_json['prefer_age_group'])
    adopter.prefer_gender = str(request_json['prefer_gender'])
    adopter.personality_preference = request_json['personality_preference']
    elderly = int(request_json['Elderly']) if request_json['Elderly'] != '' else 1
    experience = int(request_json['experience']) if request_json['experience'] != '' else 1
    kid = int(request_json['kid']) if request_json['kid'] != '' else 1
    medical = int(request_json['medical']) if request_json['medical'] != '' else 1
    other_dog = int(request_json['other_dog']) if request_json['other_dog'] != '' else 1
    window = int(request_json['window']) if request_json['window'] != '' else 1
    adopter.boring_tags = str([kid, elderly, other_dog, medical, experience, window])
    update_preference_to_db(adopter)
    query_result = query_adopter_from_db(adopter.adopter_name)
    result_json = json.loads(query_result)
    print("result_json[0][8]:", result_json[0][8])
    boring_tags = list(map(int, json.loads(result_json[0][8])))
    # result_json[0][7]: dog_index
    history_index = list(map(int, json.loads(result_json[0][7].replace("'", '"'))))
    if (result_json[0][7] == None or result_json[0][7] == "[]"):
        # result_json[0][5]:gender result_json[0][4]: age  result_json[0][3]:HDB result_json[0][6]:personality

        recommend_result = recommend_newuser(data, list(map(int, json.loads(result_json[0][5].replace("'", '"')))),
                                             list(map(int, json.loads(result_json[0][4].replace("'", '"')))),
                                             [int(adopter.accomodation)], adopter.personality_preference,
                                             boring_tags, corpus, corpus_words, 5, filter_hard=True)
    else:

        recommend_result = recommend_userhistory(data, nofilter, history_index, 5)
    adopter.recommend_dog_index = str(recommend_result)
    print("adopter.recommend_dog_index:", adopter.recommend_dog_index)
    update_recommend_dog_index_to_db(adopter)
    return get_adopter_new_recommend_response(recommend_result)


@api.route('/recommend/recommend_by_dog_index', methods=['POST'])
@cross_origin()
def recommend_by_dog_index():
    request_content = request.get_data()
    request_json = json.loads(request_content)
    print(request_json)
    adopter = Adopter()
    adopter.adopter_name = request_json['adopter_name']
    request_dog_index = request_json['dog_index']
    print("request_dog_index", request_dog_index)
    query_result = query_adopter_from_db(adopter.adopter_name)
    recommend_result = recommend_userhistory(data, nofilter, [request_dog_index], 5)
    recommend_result.insert(0, request_dog_index)
    adopter.recommend_dog_index = str(recommend_result)
    print("adopter.recommend_dog_index:", adopter.recommend_dog_index)
    update_recommend_dog_index_to_db(adopter)
    return get_adopter_new_recommend_response(recommend_result)


def create_app(app_name='SURVEY_API'):
    app = Flask(app_name)
    app.register_blueprint(api, url_prefix="/api")
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5002)