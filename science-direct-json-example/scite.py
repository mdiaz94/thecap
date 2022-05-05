import requests
import json
import arxiv

searchResults = arxiv.Search (
                query = "covid",
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
    
