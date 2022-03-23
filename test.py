from flask import Flask
from flask import render_template
import re
import datetime

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

if __name__ == '__main__':
    app.run()
    
    



@app.route("/index")
def index():
    return render_template(
        "index.html"
    )
