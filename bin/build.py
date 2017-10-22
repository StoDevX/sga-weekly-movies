#!/usr/bin/env python3
from datetime import datetime
import json
import os
import re
import urllib.parse

import pytz
from PIL import Image

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
    for day in showings['showings']:
        for time in day['times']:
            ds = f"{day['date']} {time}{offset}"
            yield {
                'time': datetime.strptime(ds, '%Y/%m/%d %H:%M%z'),
                'location': day['location'],
            }


def find_posters(folder_path, url_root):
    for f in os.scandir(folder_path):
        if not f.name.startswith('poster-'):
            continue

        with Image.open(f.path) as img:
            width, height = img.size

        yield {
            'url': f'{url_root}/{f.name}',
            'filename': f.name,
            'width': width,
            'height': height,
        }


def main():
    entries = {}

    for folder in os.scandir('movies'):
        if not folder.is_dir():
            continue

        url_root = f'{BASE}/movies/{urllib.parse.quote(folder.name)}'

        posters = sorted(list(find_posters(folder.path, url_root)), key=lambda p: p['width'])

        data = {
            'root': url_root,
            'info': load_movie_info(folder.path),
            'showings': list(load_showings_as_isoformat(folder.path)),
            'posters': posters,
        }

        entries[folder.name] = data

        with open(os.path.join(folder.path, 'index.json'), 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    dirs = sorted([m['root'] for m in entries.values()])

    with open('archive.json', 'w', encoding='utf-8') as outfile:
        data = {'movies': [f"{d}/index.json" for d in dirs]}
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    with open('next.json', 'w', encoding='utf-8') as outfile:
        data = {'movie': f"{dirs[-1]}/index.json"}
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)


if __name__ == '__main__':
    main()
