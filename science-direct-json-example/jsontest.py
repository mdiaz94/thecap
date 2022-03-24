import json

f = open('test.json')
data = json.load(f)

datatwo = data['search-results']['entry']

i = 0
for data in datatwo:
    print(datatwo[i]['dc:title'])
    print(datatwo[i]['authors'])
    print(datatwo[i]['prism:publicationName'])
    print(datatwo[i]['prism:doi'])
    i = i+1

f.close