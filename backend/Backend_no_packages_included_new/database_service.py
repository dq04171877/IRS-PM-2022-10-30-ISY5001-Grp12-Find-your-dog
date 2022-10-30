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

data = pd.read_csv('./newdata_2.csv')
shelter_adoption_data = pd.read_excel('./Shelter_Adoption_Data.xlsx')
database_path = './database.db'
schema_path = './schema.sql'

def insert_adopter_to_db(adopter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO adopter (adopter_name, password, accomodation, prefer_age_group, prefer_gender, personality_preference, boring_tags) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (adopter.adopter_name, adopter.password, adopter.accomodation,adopter.prefer_age_group, adopter.prefer_gender, adopter.personality_preference, adopter.boring_tags,))
    conn.commit()
    cursor.close()
    conn.close() 

def update_preference_to_db(adopter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE adopter SET accomodation = ?, prefer_age_group = ?, prefer_gender = ?, personality_preference = ?  WHERE adopter_name = ?",
                         (adopter.accomodation, adopter.prefer_age_group, adopter.prefer_gender, adopter.personality_preference, adopter.adopter_name, ))
    conn.commit()
    cursor.close()
    conn.close() 

def update_recommend_dog_index_to_db(adopter):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE adopter SET recommend_dog_index = ?  WHERE adopter_name = ?",
                         ( adopter.recommend_dog_index, adopter.adopter_name, ))
    conn.commit()
    cursor.close()
    conn.close() 

def is_adopter_in_db(adopter_name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_result = []
    adopter = cursor.execute("SELECT * FROM adopter WHERE adopter_name = ? AND password = ?",
                         (adopter_name,password,)).fetchall()
    for row in adopter:
        query_result.append(list(row))
    rowcount = len(adopter)
    print ('query_result:', query_result," adopter.count:", rowcount)
    conn.commit()
    cursor.close()
    conn.close()
    return rowcount == 1

def is_adopter_name_in_db(adopter_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_result = []
    adopter = cursor.execute("SELECT * FROM adopter WHERE adopter_name = ?",
                         (adopter_name,)).fetchall()
    for row in adopter:
        query_result.append(list(row))
    rowcount = len(adopter)
    print ('is_adopter_name_in_db:', query_result," adopter.count:", rowcount)
    conn.commit()
    cursor.close()
    conn.close()
    return rowcount == 1

def query_adopter_from_db(adopter_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    query_result = []
    adopter = cursor.execute("SELECT * FROM adopter WHERE adopter_name = ?",
                         (adopter_name,)).fetchall()
    query_result = json.dumps([tuple(row) for row in adopter])
    rowcount = cursor.rowcount
    cursor.close()
    conn.close()
    print ('query_result:', query_result," adopter count:", len(adopter))
    return query_result

def get_db_connection():
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection