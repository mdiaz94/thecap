from flask import Flask,redirect, session
from flask import render_template
from flask import request
import re
import datetime
import sqlite3
import models
import json
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return redirect("/index", code=302)

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

@app.route("/index", methods= ['POST', 'GET'])
def index():
    if request.method == "POST":
        search = request.form['search']
        search = search.replace("", "+")
        resultBuilder = ""
        r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query":search,"count":"50"}, headers={"Accept":"application/json","X-ELS-APIKey":"682084898b02a949777e0b81f9943e3d"})
        data = json.loads(r.content)
        print(data)
        datatwo = data['search-results']['entry']

        i = 0
        pageCounter = 1
        for data in datatwo:
            resultBuilder = resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + datatwo[i]['prism:publicationName'] + '</h6></div></div>'
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageCounter = pageCounter + 1

        return render_template("results.html", search=request.form['search'], results=resultBuilder)
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
      

'''start of login/signup'''
@app.route("/login")
def login():
    return render_template(
        "Login.html"
    )

@app.route("/signup")
def signup():
    return render_template(
        "Signup.html"
    )

@app.route('/Signdup', methods=['GET','POST'])
def Signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        print("It ran (%s)",username);
        if(password==password2):
             user = "true"
        return render_template("index.html")

app.secret_key = "xyz"

@app.route('/Signin', methods=['GET','POST'])
def Signin():
    if request.method == 'POST':
        username = request.form['Username']
        session['Username'] = username
        Username = session['Username']
        print("It ran (%s)",username);
        return render_template("index.html")

'''end of Login/Signup'''
        


if __name__ == '__main__':
    app.run()
