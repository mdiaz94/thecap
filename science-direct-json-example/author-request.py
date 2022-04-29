import arxiv

search = arxiv.Search(
  query = "computers",
  max_results = 50,
  sort_by = arxiv.SortCriterion.SubmittedDate
)

for result in search.results():
  print(result.entry_id)