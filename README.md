# microsoft-academic-crawler
Crawling [Microsoft Academic](https://www.researchgate.net/) papers' Title & Abstract info and written into a CSV file.

### Introduction
In default, the crawler will retrieve all articles with below strategy:
- Only Journal Publications, not Conference Paper, Project, or any else
- The Article must contain one of the term: `uav` or `remotesensing`
- The Article must have Abstract
- The Article is collected from year 2000 ~ 2019 (2020)

### Modifying crawling parameters
You may visit https://academic.microsoft.com/search to figure out all possible params
```python
# crawler.py
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
```

---
**Crawling for year in range. E.g., `range(2018, 2021)` will crawl for 2018, 2019, and 2020**
```python
# crawler.py
for y in range(2018, 2021):
  crawling(y)
```

### Launch the crawler

```sh
$ python crawler.py
Fetching 2014, uav = 590/613 (96%)
...
Fetching 2014, remote sensing = 600/613 (98%)
...
```

### Results
csv files, that support UTF-8 encoding, named `MicrosoftAcademic-{Term}-YYYY-YYYY-MM-DD.csv` will be created in the same location of the crawlers/caller

In which, 
- The first `Term` is the keyword to search for publications.
- The second `YYYY` is the announced year of publications.
- `YYYY-MM-DD` is the crawling date.

Ex., 
- `MicrosoftAcademic-{Term}-2007-2020-01-06.csv`
- `MicrosoftAcademic-{Term}-2008-2020-01-06.csv`
- ...

### Technology
The Crawler uses [requests](https://pypi.org/project/requests/) library to send a `POST` query to get the needed information returned in JSON format.

## Future work
Figure out to extract Keywords from Title & Abstract

**I am welcome any effort to enhance this open-source project.**

**Thank you.**