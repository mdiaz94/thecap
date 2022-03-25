import requests
import json

r=requests.get("https://api.elsevier.com/content/search/sciencedirect", params={"query":"computers"}, headers={"Accept":"application/json","X-ELS-APIKey":"64417dd6eed2d2f2d3aa7ca64942f679"})

data = json.loads(r.content)
datatwo = data['search-results']['entry']

i = 0
for data in datatwo:
    print(datatwo[i]['dc:title'])
    print(datatwo[i]['authors'])
    print(datatwo[i]['prism:publicationName'])
    print(datatwo[i]['prism:doi'])
    i = i+1
