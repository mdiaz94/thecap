from flask import Flask
from flask import render_template
from flask import request
import re
import datetime
import models
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///researchers.db'
#initialize db
db = SQLAlchemy(app)

#db model
class Researchers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



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
        models.searchPubs(searchVal)
      except:
         #redirect to home?
         render_template("index.html")

if __name__ == '__main__':
    app.run()