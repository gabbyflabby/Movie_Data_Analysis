import requests
import time
from bs4 import BeautifulSoup
import configparser
import json
import urllib.parse
import pandas as pd

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
    '''Collect given number of movies' metadata and return as a dictionary.'''
    # imdb search results url is searchable until 10,000+, so must stop at 9,951
    if total_results > 10_000:
        print('''The amount of results is too large, this function can only
        support up to 10,000. Collecting data for top 10,000 results only.''')
        total_results = 10_001
    if total_results % 50 != 0:
        print('''IMDB gives us 50 titles per search result pages. 
        As such this function can only support an amount of results divisible by
        50. Collecting first page of data.''')
        total_results = 50
    all_movies = {}
    for i in range(1,total_results,50):
        if i == 1:
            url = imdb_search_url
        else:
            url = imdb_search_url+f'&start={i}'
        movie_container = find_imdb_movies(url)
        movie_dict = collect_imdb_data(movie_container)
        all_movies.update(movie_dict)
        time.sleep(0.5)
    return all_movies

def get_api_key(config_file):
    '''Returns API key from config file'''
    config = configparser.ConfigParser()
    config.read(config_file)
    return config['API']['api_key']

def collect_moviedb_data(imdb_movie_id):
    '''Use IMDB movie IDs to search for movies on The Movie DB and update the
    movie dict with revenue and budget data.'''
    api_key = get_api_key(config_file)
    moviedb_search_url = f"https://api.themoviedb.org/3/find/{imdb_movie_id}?api_key={api_key}&language=en-US&external_source=imdb_id"
    moviedb_data = json.load(urllib.request.urlopen(moviedb_search_url))
    moviedb_movie_id = moviedb_data['movie_results'][0]['id'] if moviedb_data['movie_results'] else None
    if moviedb_movie_id:
        mdb_details_url = f'https://api.themoviedb.org/3/movie/{moviedb_movie_id}?api_key={api_key}&language=en-US'
        movie_data = json.load(urllib.request.urlopen(mdb_details_url))
        budget = movie_data['budget']
        revenue = movie_data['revenue']
    else:
        budget = 'NA'
        revenue = 'NA'
    time.sleep(0.5)
    return budget, revenue

## main ##

# all feature films of past 10 years
imdb_search_url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2010-06-30,2020-06-30'

# get moovie dict
movies = collect_all_results(imdb_search_url, 50)

imdb_movie_ids = list(movies.keys())
for xid in imdb_movie_ids:
    movies[xid]['budget'], movies[xid]['revenue'] = collect_moviedb_data(xid)

# turn movie dict into dataframe
movie_df = pd.DataFrame(list(movies.values()))

# store dataframe into pickle
movie_df.to_pickle("./movie_data.pkl")

## testing for 400 code ##
# moviedb_search_url = 'https://api.themoviedb.org/3/find/123?api_key=19ad5c6f0c75547d77ec237563fb0d7e&language=en-US&external_source=imdb_id'
# mdb_data = json.load(urllib.request.urlopen(moviedb_search_url))