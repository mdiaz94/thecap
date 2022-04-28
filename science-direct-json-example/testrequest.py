import requests
import json

r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query":"computers"}, headers={"Accept":"application/json","X-ELS-APIKey":"682084898b02a949777e0b81f9943e3d"})

data = json.loads(r.content)
datatwo = data['search-results']['entry']

i = 0
for data in datatwo:
    print(datatwo[i]['dc:title'])
    print(datatwo[i]['authors'])
    print(datatwo[i]['prism:publicationName'])
    print(datatwo[i]['prism:doi'])
    i = i+1
