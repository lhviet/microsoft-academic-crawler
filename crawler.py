import csv
import requests
import datetime

"""
Modify the below params to crawl the data we want
"""
base_url = 'https://academic.microsoft.com/api/search'
paper_url = 'https://academic.microsoft.com/paper'

headers = {'Content-Type': 'application/json; charset=utf-8'}

"""
Keywords used to search papers
Because of the limitation of Search/results from the Microsoft Academic, the search of term "drone"
returns incorrect results while requires more modifications.
Therefore, we perform the query with the two terms separately: "uav" and "remote sensing"
We also noticed that the term looks like query primarily from the Title and Category, instead of Abstract.
It means the results were filtered by Microsoft Academic may lead to the inaccuracy of further analysis.
"""
terms = ['uav', 'remote sensing']

# Type of publication we need to search is Journal Publications
publication_type = '1'

# The API allows a fixed number of 10 for each query, should not increase/decrease this limit param
limit = 10

abstract_required = True

"""
Build the Payload to pass to the query (JSON in POST method)
"""
getPayload = lambda term, offset, year: {
    "query": term,
    "queryExpression": "",
    "filters": [
        # Query articles from "Journal Publications"
        f"Pt='{publication_type}'",
        # Query articles in the year
        f"Y>={year}",
        f"Y<={year}"
    ],
    # Order by Oldest first
    "orderBy": 2,
    "skip": offset,
    # Only 10 articles returned for each request, unfortunately, we cannot change it
    "take": limit,
    "sortAscending": True,
    "includeCitationContexts": False
}

def crawl_data(term, offset, year, totalItems = 0):
  percentage = '0%' if totalItems == 0 else '{:.0%}'.format(offset/totalItems)
  print(f'Fetching {year}, {term} = {offset}/{totalItems} ({percentage})')

  res = requests.post(base_url, json=getPayload(term, offset, year), headers=headers)
  return res.json()

def crawling(year):
  author_separator = ','

  for term in terms:
    with open(f'MicrosoftAcademic-{term}-{year}-{datetime.date.today()}.csv', 'w', newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      writer.writerow(['#', 'Title', 'Authors', 'Abstract', 'Announced', 'URL', 'DOI'])

      currentOffset = 0
      totalItems = 0
      count_result = 0

      while True:
        res = crawl_data(term, currentOffset, year, totalItems)

        currentOffset += limit
        totalItems = res['t']
        dataVersion = res['dataVersion']

        if len(dataVersion) == 0:
          break

        papers = res['pr']

        for p in papers:
          p = p['paper']
          title = p['dn']

          abstract = p['d']
          if abstract_required and len(abstract) == 0:
            continue

          authors = [a['dn'] for a in p['a']]
          author_str = author_separator.join(authors)

          url = f'{paper_url}/{p["id"]}'

          count_result += 1
          data = [count_result, title, author_str, abstract, '', url]
          writer.writerow(data)

for y in range(2018, 2021):
  crawling(y)
