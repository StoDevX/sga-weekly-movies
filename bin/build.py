#!/usr/bin/env python3
from datetime import datetime
import json
import os
import re
import sys
import urllib.parse

import pytz
from colorthief import ColorThief
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
                'time': datetime.strptime(ds, '%Y-%m-%d %H:%M%z'),
                'location': day['location'],
            }


def find_posters(folder_path, url_root):
    for f in os.scandir(os.path.join(folder_path, 'poster')):
        if not (f.name.endswith('.jpg') or f.name.endswith('.png')):
            continue

        with Image.open(f.path) as img:
            width, height = img.size

        yield {
            'url': f'{url_root}/poster/{f.name}',
            'filename': os.path.join('poster', f.name),
            'width': width,
            'height': height,
        }


def find_poster_colors(folder_path, posters):
    smallest = posters[0]
    colors = ColorThief(os.path.join(folder_path, smallest['filename']))

    return {
        'dominant': colors.get_color(quality=1),
        'palette': colors.get_palette(color_count=6),
    }


def main():
    entries = {}

    for folder in os.scandir('movies'):
        if not folder.is_dir():
            continue

        print(f'processing {folder.name}', file=sys.stderr)

        url_root = f'{BASE}/movies/{urllib.parse.quote(folder.name)}'

        posters = sorted(list(find_posters(folder.path, url_root)), key=lambda p: p['width'])

        data = {
            'root': url_root,
            'info': load_movie_info(folder.path),
            'showings': list(load_showings_as_isoformat(folder.path)),
            'posters': posters,
            'posterColors': find_poster_colors(folder.path, posters),
        }

        entries[folder.name] = data

        with open(os.path.join(folder.path, 'index.json'), 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    ordered = sorted(entries.values(), key=lambda m: m['root'])

    with open('archive.json', 'w', encoding='utf-8') as outfile:
        dirs = [m['root'] for m in ordered]
        data = {'movies': [f'{d}/index.json' for d in dirs]}
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    last = ordered[-1]
    last_showing = sorted([s['time'] for s in last['showings']])[-1]
    last_showing_date = last_showing.isoformat().split('T')[0]

    with open('next.json', 'w', encoding='utf-8') as outfile:
        data = {'movie': f'{last["root"]}/index.json', 'last_showing': last_showing_date}
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)


if __name__ == '__main__':
    main()
