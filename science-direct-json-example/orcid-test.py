import requests
import json
#"access-token":"d3bb07d9-22e0-4494-a316-4ea475b93788"
#https://pub.orcid.org/v3.0/#access_token=d3bb07d9-22e0-4494-a316-4ea475b93788&token_type=bearer&expires_in=599&tokenVersion=1&persistent=true&id_token=eyJraWQiOiJwcm9kdWN0aW9uLW9yY2lkLW9yZy03aGRtZHN3YXJvc2czZ2p1am84YWd3dGF6Z2twMW9qcyIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoibDRFQ3NweldHNmNEZFVfRzJlbHRiQSIsImF1ZCI6IkFQUC05RkpZTFZWWTBENEtESTdGIiwic3ViIjoiMDAwMC0wMDAyLTY1MDEtMDc2NiIsImF1dGhfdGltZSI6MTY1MTI2MDg2MywiaXNzIjoiaHR0cHM6XC9cL29yY2lkLm9yZyIsImV4cCI6MTY1MTUxMTkwMywiZ2l2ZW5fbmFtZSI6IlRhbmltIiwiaWF0IjoxNjUxNDI1NTAzLCJmYW1pbHlfbmFtZSI6IlBhdmVsIiwianRpIjoiNTUwYTlkMmMtNTM3OS00ZTJkLWJiZWItMjM3ZThiOWE1NmNhIn0.ix9NLgvQVEiS7fjMwvn-0jt2WbBU4B9TjN_3D6viFuzSFDOl-6-mtpisftDXN8uEheDkRWDAaQebXJVmtUIgjalgppPq8yhWEX-mMkTECsYPn2rfozPsqVQ4JAyeH13Frvd6q5THkdEg7R54hPtce9uWO7CWgKfR29hRaa_xv2Cp95yJWF5BSqyPR933pNQqNn71HBGIuyR6LGxsPipo9KDURPU1Eixl_40-aSoz9EVO22BP3KkndcDwp8hV8aEdPmXI8Tv6qhNS0ai6aFQThYF233Blj1t15yWfJT3FbY7tgOtLCHtRosCf2ENzLc1aZSh4Koe5aT48OgfZXzkU2Q&tokenId=268286404

r=requests.get("https://pub.orcid.org/v3.0/0000-0002-0609-0233/works", params={}, headers={"Accept":"application/json"})
#r=requests.get("https://pub.orcid.org/v3.0/expanded-search/", params={"q":"james","rows":"50"}, headers={"Accept":"application/json"})

#r=requests.post("https://orcid.org/oauth/token", params={"client_id":"APP-9FJYLVVY0D4KDI7F","client_secret":"a5e9fad1-e79e-4003-b129-70d08cba4b65","grant_type":"client_credentials","scope":"/read-public"}, headers={"Accept":"application/json"})

#print(r.content)

file = open("orcid-search2.json", "wb")
file.write(r.content)
file.close()

f = open("out.json", encoding='utf-8')
data = json.load(f)
for research in data['group']:
    print(research['work-summary'][0]['title']['title']['value'])
    print(research['work-summary'][0]['journal-title']['value'])
    print(research['work-summary'][0]['url']['value'])
    publishDate = ""
    try:
        publishDate = publishDate + research['work-summary'][0]['publication-date']['year']['value']
    except: pass
    try:
        publishDate = publishDate + " " + research['work-summary'][0]['publication-date']['month']['value']
    except: pass
    try:
        publishDate = publishDate + " " + research['work-summary'][0]['publication-date']['day']['value']
    except: pass
    print(publishDate)