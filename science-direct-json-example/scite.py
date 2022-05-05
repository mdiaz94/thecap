import requests
import json
import arxiv
import datetime

class customResult: 
    def __init__(self, title, doi, cites, publication): 
        self.title = title
        self.doi = doi
        self.cites = cites
        self.publication = publication

searchResults = arxiv.Search (
                query = "cybersecurity",
                max_results = 100
)

doiList = []

for result in searchResults.results():
    try:
        result.doi + ""
        doiList.append(result.doi)
    except: pass

payload = "["
for i in doiList[:-1]:
    payload = payload + "\n\t\"" + i + '"' + ","
else:
    payload = payload + "\n\t\"" + i + '"'

payload = payload + "]"

response = requests.request("POST", "https://api.scite.ai/tallies", headers={}, data=payload)

data = json.loads(response.text)
doiDict = {}
for doi in data['tallies']:
    tallieDoi = data['tallies'][doi]['doi']
    talliCiting = data['tallies'][doi]['citingPublications']
    doiDict[tallieDoi] = talliCiting

customResultList = []
for result in searchResults.results():
    try:
        result.doi + ""
        customResultList.append(customResult(result.title,result.doi,doiDict[result.doi],result.journal_ref))
    except: pass

def sortFunc(e):
    return e.cites
sorted_results = customResultList
sorted_results.sort(key=sortFunc, reverse = True)

for result in sorted_results:
    print(result.title)
    print(result.publication)
    print(result.doi)
    print(result.cites)