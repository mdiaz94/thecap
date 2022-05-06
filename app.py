from pickle import NONE
from typing import Any
from flask import Flask,redirect, session, url_for
from flask import render_template
from flask import request
import sqlite3
import arxiv
from datetime import datetime
import string
import random
import requests
import json
from bs4 import BeautifulSoup
import urllib
import base64

app = Flask(__name__)
datatwo = Any
searchResults = Any
directAPI = "682084898b02a949777e0b81f9943e3d"


@app.route("/")
def home():
    return redirect("index", code=302)

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
        global searchResults
        search = request.form['search']
        search = search.replace(" ", " AND ")
        print(search)
        resultBuilder = ""
        pageBuilder = ''
        i = 0
        pageCounter = 1
        authorCounter = 0
        searchResults = arxiv.Search (
                query = search,
                max_results = 100
        )
        for result in searchResults.results():
            try:
                result.journal_ref + "test string"
                publication = result.journal_ref
            except:
                publication = 'arXiv preprint'
            publishdate = result.published.strftime('%d %B, %y')
            authorstring = ""
            for author in result.authors:
                authorstring = authorstring + author.name + ", "
            authorstring = authorstring[:-2]
            new = ' &'
            authorstring = new.join(authorstring.rsplit(",", 1))
            apaCitationBuilder = authorstring + " (" + str(result.published.year) + "). " + '"' + result.title + '"' + '. ' + publication
            apaCitationBuilder = urllib.parse.quote(apaCitationBuilder)
            mlaAuthors = ""
            if len(result.authors) == 1:
                mlaAuthors = result.authors[0].name
            if len(result.authors) >= 2:
                mlaAuthors = result.authors[0].name + ", and " + result.authors[1].name
            if len(result.authors) >= 3:
                mlaAuthors = result.authors[0].name + ", et al"
            mlaCitationBuilder = mlaAuthors + '. "' + result.title + '" ' + publication + " (" + str(result.published.year) + "). "
            mlaCitationBuilder = urllib.parse.quote(mlaCitationBuilder)
            resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + authorstring + '</h6><h6 class="card-subtitle mb-2 text-muted">' + publication + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + publishdate + 
            '</right></h6> </div><a href="/addbookmark?id=' + result.entry_id + '" type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</a>' + '<a href="/cite?apa=' + apaCitationBuilder + '&mla=' + mlaCitationBuilder + '" type="button" target="_blank" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Cite Article</a>' + '</div>')
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageBuilder = pageBuilder + '<li class="page-item"><a class="page-link" href="javascript:;" onclick="showPage(' + str(pageCounter) + ')">' + str(pageCounter) + '</a></li>'
                pageCounter = pageCounter + 1
                
        if pageCounter == 1:
            pageBuilder = ""
        return render_template("results.html", search=request.form['search'], results=resultBuilder, pages=pageBuilder, maxPageNumber=pageCounter)
    return render_template(
        "index.html"
    )

@app.route("/researcher-search", methods = ['POST','GET'])
def researcher_search():
    if request.method == 'POST':
        search = request.form['search']
        resultBuilder = ""
        pageBuilder = ''
        pageCounter = 1
        i = 0
        r = requests.get("https://pub.orcid.org/v3.0/expanded-search/", params={"q":search,"rows":"100"}, headers={"Accept":"application/json"})
        data = json.loads(r.content)
        for researcher in data['expanded-result']:
            #if statement is needed because not all researchers are active and some appraently don't have name in the orcid database
            if (researcher['institution-name'] and researcher['given-names'] and researcher['family-names'] ):
                fullName = researcher['given-names'] + " " + researcher['family-names']
                queryBuilder = "researchers?name=" + fullName + "&institution-name=" + researcher['institution-name'][0] + "&orcid-id=" + researcher['orcid-id']
                resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
                queryBuilder + '" target="_blank">' + fullName + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + researcher['institution-name'][0] + '</h6></div></div>')
                i = i + 1
                if (i % 10 == 0):
                    pageBuilder = pageBuilder + '<li class="page-item"><a class="page-link" href="javascript:;" onclick="showPage(' + str(pageCounter) + ')">' + str(pageCounter) + '</a></li>'
                    pageCounter = pageCounter + 1
                if pageCounter == 1:
                    pageBuilder = ""
        return render_template ("researcher-results.html", search=request.form['search'], results=resultBuilder, pages=pageBuilder, maxPageNumber=pageCounter)
    else:
        return render_template ("index.html")


@app.route("/filter", methods= ['POST', 'GET'])
def filter():
    if request.method == "POST":
        global searchResults
        list_results = list(searchResults.results())
        #the comment variable of an result will say if the article is in a foregin language in the same sentence as other information
        Spanish = 'in Spanish'
        French = 'in French'
        frenchlist = list(searchResults.results())
        spanishlist = list(searchResults.results())
        filtered_results = list(searchResults.results())
        frenchlist.clear()
        spanishlist.clear()
        filtered_results.clear()
        for result in list_results:
                if result.comment != None and French in result.comment:
                    frenchlist.append(result)
                if result.comment != None and Spanish in result.comment:
                    spanishlist.append(result)
        if request.form.get('English') == "one":
            for result in list_results:
                if result.comment != None and French in result.comment:
                    continue
                if result.comment != None and Spanish in result.comment:
                    continue
                filtered_results.append(result)
        if request.form.get('Spanish') == "one":
            filtered_results = filtered_results + spanishlist
        if request.form.get('French') == "one":
            filtered_results = filtered_results + frenchlist
        if (request.form.get('English') is None) and (request.form.get('Spanish') is None) and (request.form.get('French') is None):
            filtered_results=list(searchResults.results())
        if request.form.get('Date') == "one":
            def sortFunc(e):
                return e.published
            filtered_results.sort(key=sortFunc, reverse = True)
        i = 0
        pageCounter = 1
        resultBuilder = ""
        pageBuilder = ''
        for result in filtered_results:
            try:
                result.journal_ref + "test string"
                publication = result.journal_ref
            except:
                publication = 'arXiv preprint'
            publishdate = result.published.strftime('%d %B, %y')
            authorstring = ""
            for author in result.authors:
                authorstring = authorstring + author.name + ", "
            authorstring = authorstring[:-2]
            resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + authorstring + '</h6><h6 class="card-subtitle mb-2 text-muted">' + publication + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + publishdate + 
            '</right></h6> </div><a href="/addbookmark?id=' + result.entry_id + '" type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</a></div>')
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageBuilder = pageBuilder + '<li class="page-item"><a class="page-link" href="javascript:;" onclick="showPage(' + str(pageCounter) + ')">' + str(pageCounter) + '</a></li>'
                pageCounter = pageCounter + 1
                
        if pageCounter == 1:
            pageBuilder = ""
        return render_template("results.html", results=resultBuilder, pages=pageBuilder, maxPageNumber=pageCounter)
    return render_template(
        "index.html"
    )        

@app.route("/filter1", methods= ['POST', 'GET'])
def filter1():
    if request.method == "POST":
        global searchResults
        i = 0
        pageCounter = 1
        resultBuilder = ""
        pageBuilder = ''
        
        for result in searchResults.results():
            try:
            
                result.journal_ref + "test string"
                publication = result.journal_ref
            except:
                publication = 'arXiv preprint'
            publishdate = result.published.strftime('%d %B, %y')
            authorstring = ""
            for author in result.authors:
                authorstring = authorstring + author.name + ", "
            authorstring = authorstring[:-2]
            #Loops through the URLS and webscrapes all subjects, takes a good minunte for it to happen
            page=requests.get(result.entry_id)
            soup=BeautifulSoup(page.text,"html.parser")
            quotes=soup.find("span",attrs={"class" : "primary-subject"})

            resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) +'" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + authorstring + '</h6><h6 class="card-subtitle mb-2 text-muted">' + publication + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + publishdate + '</right></h6>' + '<h6 class="card-subtitle mb-2 text-muted"><right>Subject: '+ str(quotes.text) +
            '</right></h6> </div><a href="/addbookmark?id=' + result.entry_id + '" type="button" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-bookmark"></span> Bookmark</a></div>') 
            #resultBuilder = resultBuilder + '<p><a href="https://doi.org/' + datatwo[i]['prism:doi'] + '">' + datatwo[i]['dc:title'] + '</a></p>'
            i = i+1
            if (i % 10 == 0):
                pageBuilder = pageBuilder + '<li class="page-item"><a class="page-link" href="javascript:;" onclick="showPage(' + str(pageCounter) + ')">' + str(pageCounter) + '</a></li>'
                pageCounter = pageCounter + 1
                
        if pageCounter == 1:
            pageBuilder = ""
            
        return render_template("results.html", results=resultBuilder, pages=pageBuilder, maxPageNumber=pageCounter)
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
        if(num is not None):
            tem = num[0]
            print(num[0])
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
    session.pop('Username', None)
    return redirect(url_for('index'))


'''start of Topics page'''
@app.route('/Topics' , methods=['GET','POST'])
def Topics():
        string.ascii_letters
        search = random.choice(string.ascii_letters)
        print(search + ": this is the search term for 'topics'")
        resultBuilder = ""
        search = arxiv.Search (
                query = search,
                max_results = 3
        )


        #---Area for random articles
        print("test")
        authorstring = ""
        resultBuilder = "<br><h2 class='container-md'>Recently Published Articles to Explore</h2>"
        for result in search.results():
            print("test")
            print(result.title)

            for author in result.authors:
                authorstring = authorstring + author.name + ", "
            authorstring = authorstring[:-2]

            resultBuilder = (resultBuilder + '<div class="card' + " page" + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + '</a></h5><h6 class="card-subtitle mb-2 text-muted"> AUTHORS: ' + authorstring + '</h6><h6 class="card-subtitle mb-2 text-muted">' + 
            '</right></h6> </div></div>')
        
        #---Area for Science articles
        authorstringScience = ""
        resultBuilder = resultBuilder + "<br><h2 class='container-md'>Recent Topics to Explore in SCIENCE</h2>"   
        searchScience = arxiv.Search (
                query = "Science",
                max_results = 3,
                sort_by = arxiv.SortCriterion.SubmittedDate
        )
        for result in searchScience.results():
            print("test")
            print(result.title)

            for author in result.authors:
                authorstringScience = authorstringScience + author.name + ", "
            authorstringScience = authorstringScience[:-2]

            resultBuilder = (resultBuilder + '<div class="card' + " page" + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + '</a></h5><h6 class="card-subtitle mb-2 text-muted"> AUTHORS: ' + authorstringScience + '</right></h6> </div></div>')
        #---Area for Technology
        authorstringTechnology = ""
        resultBuilder = resultBuilder + "<br><h2 class='container-md'>Recent Topics to explore in TECHNOLOGY</h2>"  
        searchTechnology = arxiv.Search (
                query = "Technology",
                max_results = 3,
                sort_by = arxiv.SortCriterion.SubmittedDate
        )
        for result in searchTechnology.results():
            print("test")
            print(result.title)

            for author in result.authors:
                authorstringTechnology = authorstringTechnology + author.name + ", "
            authorstringTechnology = authorstringTechnology[:-2]

            resultBuilder = (resultBuilder + '<div class="card' + " page" + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + 
            result.entry_id + '">' + result.title + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' + '</a></h5><h6 class="card-subtitle mb-2 text-muted"> AUTHORS: ' + authorstringTechnology   + '</right></h6> </div></div>')
       




        print(resultBuilder)
        return render_template("Topics.html", search=search, results=resultBuilder)
        #return resultBuilder

            


'''bookmark page'''
@app.route("/addbookmark")
def addBookmark():
    if request.method == 'GET':
        if('Username' not in session):
            return redirect("/login")
        conn = sqlite3.connect("Users.db")
        c = conn.cursor()
        username = (session['Username'])
        book = str(request.url)
        book = book.split("?id=")
        link = book[1]
        link = urllib.parse.unquote_plus(link)
        c.execute("INSERT INTO bookmark VALUES('%s','%s')"%(link,username))
        conn.commit()
        conn.close()
    return redirect("/bookmarks")

@app.route("/bookmarks")
def bookmark():
    conn = sqlite3.connect("Users.db")
    c = conn.cursor()
    username = (session['Username'])
    c.execute("SELECT * FROM bookmark WHERE name = '%s';"%(username))
    bookmarks = c.fetchall()
    temp = ""
    if(bookmarks is not None):
            for bookmark in bookmarks:
                temp = temp + '<div class="card' + " page" + '" style="width: 70%;"><div class="card-body"><h5 class="card-title"><a href="' + bookmark[0] + '">' + bookmark[0] + '</a></h5><h6 class="card-subtitle mb-2 text-muted">' +  '</h6></div></div>'
    if(bookmarks is None):
            temp = "There are none"
    conn.commit()
    conn.close()
    return render_template("bookmarks.html",bookmark = temp)

'''end of Topics page'''
@app.route("/researchers")
def research():
    args = request.args
    args = args.to_dict()
    researcherName = args.get('name')
    researcherInstitution = args.get('institution-name')
    orcid = args.get('orcid-id')
    resultBuilder = ""
    pageBuilder = ''
    pageCounter = 1
    i = 0
    noArticles = ""
    orcidURL = "https://pub.orcid.org/v3.0/" + orcid + "/works"
    r=requests.get(orcidURL, params={}, headers={"Accept":"application/json"})
    data = json.loads(r.content)
    for research in data['group']:
        articleTitle = research['work-summary'][0]['title']['title']['value']
        try:
            journalTitle = research['work-summary'][0]['journal-title']['value']
        except:
            journalTitle = ""
        try:
            articleURL = research['work-summary'][0]['url']['value']
        except:
            articleURL = ""
        publishDate = ""
        try:
            publishDate = publishDate + research['work-summary'][0]['publication-date']['year']['value']
        except: pass
        try:
            publishDate = publishDate + "-" + research['work-summary'][0]['publication-date']['month']['value']
        except: pass
        try:
            publishDate = publishDate + "-" + research['work-summary'][0]['publication-date']['day']['value']
        except: pass
        if articleURL == "":
            articleURL = articleTitle
        else:
            articleURL = '<a href="' + articleURL + '">' + articleTitle + '</a>'
        resultBuilder = (resultBuilder + '<div class="card' + " page" + str(pageCounter) + '" style="width: 70%;"><div class="card-body"><h5 class="card-title">' + articleURL 
        + '</h5></h6><h6 class="card-subtitle mb-2 text-muted">' + journalTitle + '</h6><h6 class="card-subtitle mb-2 text-muted"><right>Date Published: ' + publishDate + 
            '</right></h6> </div></div>')
        i = i + 1
        if (i % 10 == 0):
            pageBuilder = pageBuilder + '<li class="page-item"><a class="page-link" href="javascript:;" onclick="showPage(' + str(pageCounter) + ')">' + str(pageCounter) + '</a></li>'
            pageCounter = pageCounter + 1
        if pageCounter == 1:
            pageBuilder = ""
    if resultBuilder == "":
        noArticles = '1'
    return render_template(
        "research.html", researcherName = researcherName, researcherInstitution = researcherInstitution, results=resultBuilder, pages=pageBuilder, maxPageNumber=pageCounter, noArticles=noArticles
    )

@app.route("/cite")
def cite():
    args = request.args
    args = args.to_dict()
    apa = args.get('apa')
    mla = args.get('mla')
    return render_template ("cite.html", apa=apa, mla=mla)


if __name__ == '__main__':
    app.run()
