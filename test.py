from flask import Flask
from flask import render_template
import re
import datetime
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

if __name__ == '__main__':
    app.run()
    



@app.route("/index")
def index():
    return render_template(
        "index.html"
    )