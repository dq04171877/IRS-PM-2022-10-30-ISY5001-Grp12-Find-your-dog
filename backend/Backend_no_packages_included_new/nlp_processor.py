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

def my_preprocessing(raw_sentence):
    nlp_tool = spacy.load('en_core_web_sm')
    # nlp_tool = en_core_web_sm.load()
    token_sentence = nlp_tool(raw_sentence.lower())
    with open('./irrelevant_words.txt') as file:
        irrelevantlist = [stopword.replace('\n', '').lower() for stopword in file.readlines()]
    #     new_sentence = [word for word in token_sentence if word not in irrelevantlist]

    preprocessed_sentence = []

    for token in token_sentence:
        if token.pos_ == "PUNCT" or token.is_stop == True or token.is_alpha == False or token.pos_ == "SYM":
            continue

        elif token.lemma_ in irrelevantlist or len(token) == 1:
            continue

        else:
            preprocessed_sentence.append(token.lemma_)

    return preprocessed_sentence