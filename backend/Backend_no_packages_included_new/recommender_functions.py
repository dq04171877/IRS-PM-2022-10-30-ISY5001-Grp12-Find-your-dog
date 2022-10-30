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

data = pd.read_csv('./newdata_2.csv')
shelter_adoption_data = pd.read_excel('./Shelter_Adoption_Data.xlsx')
database_path = './database.db'
schema_path = './schema.sql'

def filter_dog(data, gender, age, hdb):
    filtered = []
    if hdb == 0:
        hdb_ = [0, 1]
    else:
        hdb_ = [1]
    for i in range(335):
        if data.loc[i, 'Gender'] in gender:
            if data.loc[i, 'Age'] in age:
                if data.loc[i, 'HDB'] in hdb_:
                    filtered.append(i)
    return filtered

def cosine_similarity(dogx, dogy, hard_constraint, soft_constraint, tfidf, user):
    numerator = 0
    denominator_x = 0
    denominator_y = 0
    if hard_constraint == True:
        numerator += dogx['Gender'] * dogy[indexy]['Gender']
        numerator += dogx[indexx]['Age'] * dogy[indexy]['Age']
        numerator += dogx[indexx]['HDB'] * dogy[indexy]['HDB']
        denominator_x += dogx[indexx]['Gender'] ** 2
        denominator_x += dogx[indexx]['Age'] ** 2
        denominator_x += dogx[indexx]['HDB'] ** 2
        denominator_y += dogy[indexx]['Gender'] ** 2
        denominator_y += dogy[indexx]['Age'] ** 2
        denominator_y += dogy[indexx]['HDB'] ** 2
    if soft_constraint == True:
        for i in range(6):
            if user == True:
                tagix = dogx['Tag' + str(i + 3)]
                tagiy = dogy['Tag' + str(i + 3)]
                if dogx['Tag' + str(i + 3)] == 0 or dogy['Tag' + str(i + 3)] != 0:
                    tagix = 0
                    tagiy = 0
            numerator += tagix * tagiy
            denominator_x += tagix ** 2
            denominator_y += tagiy ** 2
    if tfidf == True:
        for i in range(1770):
            numerator += dogx['tfidf' + str(i)] * dogy['tfidf' + str(i)]
            denominator_x += dogx['tfidf' + str(i)] ** 2
            denominator_y += dogy['tfidf' + str(i)] ** 2

    denominator_x = math.sqrt(denominator_x)
    denominator_y = math.sqrt(denominator_y)
    if denominator_x * denominator_y == 0:
        return 0
    return (numerator / (denominator_x * denominator_y))

# Based on user's history data, build a user's prefernce.
# The return is a list
def user_history(data, dogs_index):
    history = []
    history.append(999)
    history.append('History')
    history.append(0)
    history.append(0)
    history.append(0)
    history.append('courpus')
    for i in range(6):
        history.append(0)
    for i in range(1770):
        summ = 0
        average = 0
        for index in dogs_index:
            summ += data.loc[index]['tfidf' + str(i)]
        average = summ / len(dogs_index)
        history.append(average)
    #     data.loc[335] = history
    return history


# ## Recommender for old users based on the user's history prefernece

# In[ ]:


# Find the similar dogs according to cosine similarity
def recommend_userhistory(data, dogs_filter_index, history_index, target_num):
    similarity = []
    history = user_history(data, history_index)
    data.loc[999] = history
    print('History preference made')
    #     num = 1
    for index in history_index:
        if index in dogs_filter_index:
            #             print(index)
            dogs_filter_index.remove(index)
    for index in dogs_filter_index:
        cos_sim = cosine_similarity(data.loc[index], data.loc[999], hard_constraint=False, soft_constraint=False,
                                    tfidf=True, user=False)
        #         print(str(num) + '/' + str(len(dogs_filter_index)) + ' : ' + str(cos_sim))
        #         num += 1
        similarity.append(cos_sim)
    #     print(similarity)
    max_index_ = list(map(similarity.index, heapq.nlargest(target_num, similarity)))
    max_index = []
    for i in range(len(max_index_)):
        max_index.append(dogs_filter_index[max_index_[i]])
    max_value = heapq.nlargest(target_num, similarity)
    return max_index


def process_user_description(description, corpus_words):
    des = ''
    sentence = my_preprocessing(description)
    #     print(sentence)
    for word in sentence:
        if word in corpus_words:
            des += ' '
            des += word
    #     print(des)
    return des


def new_user_tfidf_list(des, corpus):
    corpus_new = []
    corpus_new.append(des)
    for text in corpus:
        corpus_new.append(text)
    #     print(len(corpus_new))
    vectorizer = CountVectorizer()
    word_vec = vectorizer.fit_transform(corpus_new)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(word_vec)
    tfidf_matrix = tfidf.toarray()
    #     print(tfidf_matrix.shape)
    return tfidf_matrix[0]





# In[ ]:


def build_new_user(description, tags, corpus, corpus_words):
    user = []
    user.append(666)
    user.append('NewUser')
    user.append(0)
    user.append(0)
    user.append(0)
    des = process_user_description(description, corpus_words)
    #     print(des)
    user.append(des)
    for i in tags:
        user.append(i)
    for i in new_user_tfidf_list(des, corpus):
        user.append(i)
    return user


# data.loc[666] = build_new_user('cute lovely shy quiet',[1,1,1,1,1,1],corpus,corpus_words)


# In[ ]:


def recommend_newuser(data, gender, age, hdb, description, tags, corpus, corpus_words, target_num, filter_hard):
    #     print(description)
    #     print(tags)
    if tags == []:
        tags = [1, 1, 1, 1, 1, 1]
    #     print(tags)
    data.loc[666] = build_new_user(description, tags, corpus, corpus_words)
    if filter_hard == True:
        filtered_index = filter_dog(data, gender, age, hdb)
    else:
        filtered_index = filter_dog(data, [0, 1], [0, 1, 2, 3], [0, 1])
    similarity = []
    #     print('Dogs after filtering:' + str(filtered_index))

    for index in filtered_index:
        cos_sim = cosine_similarity(data.loc[index], data.loc[666], hard_constraint=False, soft_constraint=True,
                                    tfidf=True, user=True)
        similarity.append(cos_sim)
    #     for i in range(len(similarity)):
    #         print('similarity for index ' + str(filtered_index[i])+ ' : ' +str(similarity[i]))
    max_index_ = list(map(similarity.index, heapq.nlargest(target_num, similarity)))
    max_index = []
    num = min(target_num, len(filtered_index))
    for i in range(len(max_index_)):
        max_index.append(filtered_index[max_index_[i]])
    max_value = heapq.nlargest(num, similarity)
    #     print(len(max_index))
    #     max_value = [0,0,0,0,0] #try all 0
    return_null = 1
    for i in range(num):
        if max_value[i] != 0:
            return_null = 0
    if return_null == 1:
        return []
    for i in range(num):
        if max_value[num - i - 1] == 0:
            #             print(len(max_index)-i-1)
            max_index.pop(num - i - 1)
            max_value.pop(num - i - 1)
    return max_index