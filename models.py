# app.py
from flask import render_template

import sqlite3
connection = sqlite3.connect('Users.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE [IF NOT EXISTS] users (user_id INTEGER PRIMARY KEY,name TEXT NOT NULL,password TEXT [WITHOUT ROWID];")
cursor.execute("CREATE TABLE [IF NOT EXISTS] resarchers (researcher_id INTEGER PRIMARY KEY,name TEXT NOT NULL [WITHOUT ROWID];")
cursor.execute("CREATE TABLE [IF NOT EXISTS] publications (publication_id INTEGER PRIMARY KEY,name TEXT, FOREIGN KEY(author) REFERENCES researchers(researcher_id) [WITHOUT ROWID];")
connection.commit()


def searchPubs(search):
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute("select * from publications WHERE title contains ?", search)
   rows = cur.fetchall(); 
   #rows are multidict object
   return render_template("results.html",rows = rows)
   


