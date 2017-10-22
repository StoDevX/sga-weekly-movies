#!/usr/bin/env python3
from datetime import datetime
import json
import os
import re
import urllib.parse

import pytz

BASE = 'https://stodevx.github.io/sga-weekly-movies'


def now():
    return datetime.now(tz=pytz.timezone('America/Winnipeg'))


def json_serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def load_movie_info(folder_path):
    with open(os.path.join(folder_path, 'movie.json'), 'r', encoding='utf-8') as infile:
        movie = json.load(infile)

    del movie["Metascore"]
    del movie["imdbRating"]
    del movie["imdbVotes"]
    del movie["imdbID"]
    del movie["Poster"]

    return movie


def load_showings_as_isoformat(folder_path):
    with open(os.path.join(folder_path, 'showings.json'), 'r', encoding='utf-8') as infile:
        showings = json.load(infile)

    offset = now().strftime('%z')
    return [datetime.strptime(f"{day['date']} {time}{offset}", '%Y/%m/%d %H:%M%z')
            for day in showings['showings']
            for time in day['times']]


def find_posters(folder_path):
    return {re.sub(r'poster-(\d+).jpg', r'\1', f.name): f.name
            for f in os.scandir(folder_path)
            if f.name.startswith('poster-')}


def main():
    entries = {}

    for folder in os.scandir('movies'):
        if not folder.is_dir():
            continue

        data = {
            'root': f'{BASE}/movies/{urllib.parse.quote_plus(folder.name)}',
            'info': load_movie_info(folder.path),
            'showings': load_showings_as_isoformat(folder.path),
            'posters': find_posters(folder.path),
        }

        entries[folder.name] = data

        with open(os.path.join(folder.path, 'index.json'), 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    dirs = sorted([m['root'] for m in entries.values()])

    with open('archive.json', 'w', encoding='utf-8') as outfile:
        json.dump({'movies': dirs}, outfile, default=json_serialize, ensure_ascii=False)

    with open('next.json', 'w', encoding='utf-8') as outfile:
        json.dump({'movie': f"{dirs[-1]}/index.json"}, outfile, default=json_serialize, ensure_ascii=False)


if __name__ == '__main__':
    main()
