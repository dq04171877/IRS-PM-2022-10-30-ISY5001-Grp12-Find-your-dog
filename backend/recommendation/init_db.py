import sqlite3

connection = sqlite3.connect('database.db')

with open('recommendation/schema.sql') as f:
    connection.executescript(f.read())
