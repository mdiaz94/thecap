from flask import Flask
from flask import render_template
from flask import request
import re
import datetime
import sqlite3
import models
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "testtemp.html",
        name=name
    )

@app.route("/testarea")
def testTemp():
    return render_template(
        "index.html"
    )

@app.route("/index")
def index():
    return render_template(
        "index.html"
    )

@app.route('/search', methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      try:
        #cant figure out how to get searchvalue from form passed into this searchVal variable so i hard coded it to tzit no matter .
        #what was inputted to the search box There are test records in publications and 2 of them have the word tzit somewhere in the title
        #searchVal = request.form['search']
        searchVal = request.form['search']
        con = sqlite3.connect("Users.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM publications WHERE title LIKE ?;", ("%"+searchVal+"%",))
        rows = cur.fetchall(); 
        return render_template("results.html", rows = rows)
      except:
         #redirect to home?
         print("there was an oopsy")
         return render_template("index.html")
      

        

if __name__ == '__main__':
    app.run()
