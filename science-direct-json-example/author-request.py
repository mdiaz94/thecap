import arxiv

search = arxiv.Search(
  query = "computers",
  max_results = 1,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
  authorstring = ""
  for author in result.authors:
    authorstring = authorstring + author.name + ", "
  authorstring = authorstring[:-2]
  print(authorstring)