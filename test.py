from turtle import right
from typing import Any
from flask import Flask,redirect, session, url_for
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
datatwo = Any
search = Any
directAPI = "682084898b02a949777e0b81f9943e3d"


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
        global search
        search = request.form['search']
        search = search.replace("", "+")
        resultBuilder = ""
        r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query":search,"count":"50"}, headers={"Accept":"application/json","X-ELS-APIKey":directAPI})
        data = json.loads(r.content)#all the data in a giant variable
        #print(data)
        global datatwo
        datatwo = data['search-results']['entry']#defines the search results so we can cut it up
        i = 0
        pageCounter = 1
        
        for data in datatwo:
            resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="https://doi.org/' + 
            datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + datatwo[i]['prism:publicationName'] + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + datatwo[i]['prism:coverDate'] + '</right></h6> </div><button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</button></div>')
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageCounter = pageCounter + 1

        return render_template("results.html", search=request.form['search'], results=resultBuilder)
    return render_template(
        "index.html"
    )

@app.route("/filter", methods= ['POST', 'GET'])
def filter():
    if request.method == "POST":
        global datatwo
        filteredData = datatwo
        if request.form['Date'] == "one":
            def sortFunc(e):
                return e['prism:coverDate']
            filteredData.sort(key=sortFunc, reverse = True)
        i = 0
        pageCounter = 1
        resultBuilder = ""
        for data in filteredData:
            resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="https://doi.org/' + 
            filteredData[i]['prism:doi'] + '">' + filteredData[i]['dc:title'] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + filteredData[i]['prism:publicationName'] + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + filteredData[i]['prism:coverDate'] + '</right></h6> </div><button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</button></div>')
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageCounter = pageCounter + 1

        return render_template("results.html", search=search, results=resultBuilder)
    return render_template(
        "index.html"
    )

@app.route('/search', methods = ['POST', 'GET'])
def searchFuture():
    #not using this code rn
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

@app.route('/signup', methods=['GET','POST'])
def Signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if(password==password2):
            conn = sqlite3.connect("Users.db")
            c = conn.cursor()
            c.execute("SELECT Count(*) FROM users;")
            num = c.fetchone()
            hi = int(num[0])
            hi+=1
            c.execute("INSERT INTO users VALUES(%d,'%s','%s')"%(hi,username,password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        return render_template("Signup.html")

app.secret_key = "xyz"

@app.route('/login', methods=['GET','POST'])
def Signin():
    if request.method == 'POST':       
        username = request.form['Username']
        pasword = request.form['password']
        conn = sqlite3.connect("Users.db")
        c = conn.cursor()
        c.execute("SELECT name FROM users WHERE name = '%s' AND password = '%s';"%(username,pasword))
        num = c.fetchone()
        tem = num[0]
        print(tem)
        if(tem == username):
            session['Username'] = username
            Username = session['Username']
            session['logged_in'] = True
            return redirect(url_for('index'))
    return redirect(url_for('login'))
'''end of Login/Signup'''
        
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


'''start of Topics page'''
@app.route('/Topics' , methods=['GET','POST'])
def Topics():
    searchTwo = "a"
    resultBuilder = ""
    r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query": searchTwo,"count":"3"}, headers={"Accept":"application/json","X-ELS-APIKey":"682084898b02a949777e0b81f9943e3d"})
    data = json.loads(r.content)#all the data in a giant variable
    #print(data)
    global datatwo
    datatwo = data['search-results']['entry']#defines the search results so we can cut it up
    i = 0
    pageCounter = 1
   
    for data in datatwo:
        resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="https://doi.org/' + 
        datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + datatwo[i]['prism:publicationName'] + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + datatwo[i]['prism:coverDate'] + '</right></h6> </div><button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</button></div>')
        print(datatwo[i]['dc:title'])
        print(datatwo[i]['authors'])
        print(datatwo[i]['prism:publicationName'])
        print(datatwo[i]['prism:doi'])
        datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + datatwo[i]['prism:publicationName'] + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + datatwo[i]['prism:coverDate'] + '</right></h6> </div><button type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</button></div>' 
        #print(datatwo[i]['dc:title'])
        #print(datatwo[i]['authors'])
        #print(datatwo[i]['prism:publicationName'])
        #print(datatwo[i]['prism:doi'])
        i = i+1
        
    return render_template("Topics.html", search=searchTwo, results=resultBuilder)


    

    

'''end of Topics page'''
@app.route("/researchers")
def research():
    return render_template(
        "research.html"
    )


if __name__ == '__main__':
    app.run()
