# app.py
from flask import render_template

import sqlite3
connection = sqlite3.connect('Users.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,name TEXT NOT NULL,password TEXT);")
cursor.execute("CREATE TABLE IF NOT EXISTS resarchers (researcher_id INTEGER PRIMARY KEY,name TEXT NOT NULL);")
cursor.execute("CREATE TABLE IF NOT EXISTS publications (publication_id INTEGER PRIMARY KEY,name TEXT, author_id INTEGER, FOREIGN KEY(author_id) REFERENCES researchers(researcher_id));")
connection.commit()
connection.close()

def searchPubs(search):
   con = sqlite3.connect("Users.db")
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   cur.execute(" Declare @userinput as varchar(50) Set @userinput = ? Select * From publications where title Like '%' + LTRIM(RTRIM(@userinput)) + '%'", search)
   rows = cur.fetchall(); 
   #rows are multidict object
   return rows