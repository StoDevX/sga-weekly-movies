import requests
import sys
from .keys import TMDB_API_KEY


def get_trailers(imdb_id):
    params = {'language': 'en-US', 'api_key': TMDB_API_KEY}
    url = f'https://api.themoviedb.org/3/movie/{imdb_id}/videos'
    r = requests.get(url, params=params)

    data = r.json()

    if 'status_message' in data:
        if data['status_code'] is 34:
            print(f'The IMDB ID {imdb_id} was not present in TMDB\'s db. Continuing without trailers.',
                  file=sys.stderr)
            return []
        else:
            print('TMDB API error:', file=sys.stderr)
            print(data['status_message'], file=sys.stderr)
            sys.exit(1)

    if 'results' not in data:
        print('No trailers found! Continuing without them.', file=sys.stderr)
        return []

    for trailer in data['results']:
        del trailer['id']
        if trailer['site'] == 'YouTube':
            trailer['url'] = f'https://www.youtube.com/watch?v={trailer["key"]}'
        else:
            trailer['url'] = None
        yield trailer
