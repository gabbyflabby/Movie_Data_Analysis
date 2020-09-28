import requests
from bs4 import BeautifulSoup

# past 10 years
imdb_search_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2010-06-30,2020-06-30'
config_file = 'config.py'

html_page = requests.get(imdb_search_url)
html_tree = BeautifulSoup(html_page.content, 'html.parser')