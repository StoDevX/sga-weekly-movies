import requests
from pick import pick

from .keys import OMDB_API_KEY


def get_movie(imdbID):
    params = {'i': imdbID, 'apiKey': OMDB_API_KEY, 'plot': 'short'}
    r = requests.get('http://www.omdbapi.com/', params=params)
    results = r.json()
    return results


def find_movie(title, year):
    params = {'s': title, 'apiKey': OMDB_API_KEY, 'type': 'movie'}
    if year:
        params['y'] = year

    r = requests.get('http://www.omdbapi.com/', params=params)
    results = r.json()
    options = [f'{m["Title"]} ({m["Year"]}) <{m["Poster"]}>' for m in results['Search']]

    [chosen_title, chosen_index] = pick(options)

    chosen_movie = results['Search'][chosen_index]

    return get_movie(chosen_movie['imdbID'])
