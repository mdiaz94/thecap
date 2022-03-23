# app.py

import sqlite3
connection = sqlite3.connect('Users.db')
cursor = connection.cursor()
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users
              (ID,Username, password)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Bookmarks
              (ID, bookmark)''')
connection.commit()
connection.close()
