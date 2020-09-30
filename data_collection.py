import requests
from bs4 import BeautifulSoup

# all feature films of past 10 years
imdb_search_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2010-06-30,2020-06-30'


config_file = 'config.py'

def find_imdb_movies(imdb_search_url):
    '''Create a movie container from IMDB search results.'''
    html_page = requests.get(imdb_search_url)
    html_tree = BeautifulSoup(html_page.content, 'html.parser')
    # list of movies from imdb page
    movie_container = html_tree.find_all('div', class_='lister-item-content')
    return movie_container

def collect_imdb_data(movie_container):
    '''Collect movie metadata and return as a dictionary.'''
    movie_dict = {}
    for movie in movie_container:
        # if info does not exist, set to NA
        title = movie.find('a').get_text() if movie.find('a') else 'NA'
        movie_dict[title] = {
            'mpaa_rating': movie.find('span', class_='certificate').get_text() if movie.find('span', class_='certificate') else 'NA',
            'runtime': movie.find('span', class_='runtime').get_text() if movie.find('span', class_='runtime') else 'NA',
            'genre': movie.find('span', class_='genre').get_text() if movie.find('span', class_='genre') else 'NA',
            'star_rating': movie.find('strong').get_text() if movie.find('strong') else 'NA',
            'imdb_id': movie.find('a').attrs['href'].replace('title', '').strip('/')
        }
    return movie_dict

movie_container = find_imdb_movies(imdb_search_url)
movie_dict = collect_imdb_data(movie_container)
print(movie_dict)