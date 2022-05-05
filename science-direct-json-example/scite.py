import requests
import json
import arxiv
import datetime

start_time = datetime.datetime.now()

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
print(payload)

response = requests.request("POST", "https://api.scite.ai/tallies", headers={}, data=payload)

data = json.loads(response.text)
doiDict = {}
for doi in data['tallies']:
    tallieDoi = data['tallies'][doi]['doi']
    talliCiting = data['tallies'][doi]['citingPublications']
    doiDict[tallieDoi] = talliCiting

sortedDoiDict = {}
sortedDoiDictKey = sorted(doiDict, key=doiDict.get, reverse=True)

for w in sortedDoiDictKey :
    sortedDoiDict[w] = doiDict[w]

print(sortedDoiDict)

for x in sortedDoiDict:
    articleTitle = ""
    for result in searchResults.results():
        if result.doi == x:
            articleTitle = result.title
            break
    if articleTitle == "":
        pass
    else:
        print(articleTitle)
        print(x)
        print(sortedDoiDict[x])

end_time = datetime.datetime.now()

time_diff = (end_time - start_time)

execution_time = time_diff.total_seconds() * 1000

print(execution_time)