import requests
import time
from bs4 import BeautifulSoup

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
        imdb_id = movie.find('a').attrs['href'].replace('title', '').strip('/')
        movie_dict[imdb_id] = {
            'title': movie.find('a').get_text() if movie.find('a') else 'NA',
            'mpaa_rating': movie.find('span', class_='certificate').get_text() if movie.find('span', class_='certificate') else 'NA',
            'runtime': movie.find('span', class_='runtime').get_text() if movie.find('span', class_='runtime') else 'NA',
            'genre': movie.find('span', class_='genre').get_text() if movie.find('span', class_='genre') else 'NA',
            'star_rating': movie.find('strong').get_text() if movie.find('strong') else 'NA',
        }
    return movie_dict

def collect_all_results(imdb_search_url, total_results):
    # imdb search results url is searchable until 10,000+, so must stop at 9,951
    if total_results > 10_000:
        print('The amount of results is too large, this function can only support up to 10,000. Collecting data for top 10,000 results only.')
        total_results = 10_001
    all_movies = {}
    for i in range(1,total_results,50):
        if i == 1:
            url = imdb_search_url
        else:
            url = imdb_search_url+f'&start={i}&ref_=adv_nxt'
        movie_container = find_imdb_movies(url)
        movie_dict = collect_imdb_data(movie_container)
        all_movies.update(movie_dict)
        time.sleep(0.5)
    return all_movies

## main ##

# all feature films of past 10 years
imdb_search_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2010-06-30,2020-06-30'

movies = collect_all_results(imdb_search_url, 10_000)

count = 1
for movie in movies.items():
    print(f'{count}. {movie[0]}, {movie[1]}')
    count += 1