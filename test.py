from flask import Flask
from flask import render_template
from flask import request
import re
import datetime
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
   if request.method == 'GET':
      try:
        searchVal = request.form['search']
        rows = models.searchPubs(searchVal)
        return render_template("results.html", rows = rows)
      except:
         #redirect to home?
         return render_template("index.html")  
        

if __name__ == '__main__':
    app.run()