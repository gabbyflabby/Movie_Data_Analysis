import requests
from bs4 import BeautifulSoup

# all feature films of past 10 years
imdb_search_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2010-06-30,2020-06-30'


config_file = 'config.py'

html_page = requests.get(imdb_search_url)
html_tree = BeautifulSoup(html_page.content, 'html.parser')

# list of movies from imdb page
movies = html_tree.find_all('div', class_='lister-item-content')

# collect movie metadata and put into dictionary
movie_dict = {}
for movie in movies:
    # if info does not exist, set to NA
    title = movie.find('a').get_text() if movie.find('a') else 'NA'
    movie_dict[title] = {
        'mpaa_rating': movie.find('span', class_='certificate').get_text() if movie.find('span', class_='certificate') else 'NA',
        'runtime': movie.find('span', class_='runtime').get_text() if movie.find('span', class_='runtime') else 'NA',
        'genre': movie.find('span', class_='genre').get_text() if movie.find('span', class_='genre') else 'NA',
        'star_rating': movie.find('strong').get_text() if movie.find('strong') else 'NA',
        'imdb_id': movie.find('a').attrs['href']
    }