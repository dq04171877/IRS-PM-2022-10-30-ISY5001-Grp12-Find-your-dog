"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from unicodedata import name
from flask import Blueprint, jsonify, request
import sqlite3

api = Blueprint('api', __name__)

@api.route('/hello/<string:name>/')
def say_hello(name):
    response = { 'msg': "Hello {}".format(name) }
    return jsonify(response)

@api.route('/recommend/query/<string:name>')
def queryTitle(name):
    conn = get_db_connection()
    name = name.replace("%20", " ")
    data = []
    posts = conn.execute("SELECT * FROM posts WHERE title = '%s'"%name).fetchall()
    for row in posts:
        data.append(list(row))
    conn.close()
    return jsonify(data)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection
  
