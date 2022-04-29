import requests
import json

r=requests.get("https://api.elsevier.com/content/search/author", params={"query":"james","apiKey":"64417dd6eed2d2f2d3aa7ca64942f679"}, headers={"Accept":"application/json","X-ELS-APIKey":"169774cc940465ade087633980bd2421"})

data = json.loads(r.content)
#datatwo = data['search-results']['entry']
print(data)
