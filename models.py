# app.py
from flask import render_template

import sqlite3
connection = sqlite3.connect('Users.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,name TEXT NOT NULL,password TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS researchers (researcher_id INTEGER PRIMARY KEY,name TEXT NOT NULL);")
cursor.execute("CREATE TABLE IF NOT EXISTS publications (publication_id INTEGER PRIMARY KEY,title TEXT,author_id INTEGER, FOREIGN KEY(author_id) REFERENCES researchers(researcher_id));")
cursor.execute("CREATE TABLE IF NOT EXISTS bookmark (bookmark TEXT NOT NULL,name TEXT NOT NULL);")
connection.commit()
connection.close()