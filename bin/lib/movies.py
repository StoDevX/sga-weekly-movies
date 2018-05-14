import requests

try:
    import dialogs
    from ui import ListDataSource
    is_pythonista = True
except ModuleNotFoundError:
    from pick import pick
    is_pythonista = False

from .keys import OMDB_API_KEY


def get_movie(imdb_id):
    params = {'i': imdb_id, 'apiKey': OMDB_API_KEY, 'plot': 'short'}
    r = requests.get('http://www.omdbapi.com/', params=params)
    return r.json()


def search_for_movie(title: str, year: int):
    params = {'s': title, 'apiKey': OMDB_API_KEY, 'type': 'movie'}
    if year:
        params['y'] = year

    r = requests.get('http://www.omdbapi.com/', params=params)
    results = r.json()
    
    print(results)

    if is_pythonista:
        options = [{
            'title': f'{m["Title"]} ({m["Year"]})',
            'accessory_type': 'disclosure_indicator',
        } for m in results['Search']]

        chosen_title = dialogs.list_dialog('Pick one', options)
        if not chosen_title:
            return None

        chosen_index = options.index(chosen_title)
    else:
        options = [f'{m["Title"]} ({m["Year"]})' for m in results['Search']]
        [chosen_title, chosen_index] = pick(options)

    chosen_movie = results['Search'][chosen_index]

    return get_movie(chosen_movie['imdbID'])
