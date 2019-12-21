#!/usr/bin/env python3

from datetime import datetime, date, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
import pathlib
import sys
import urllib.parse

import pytz
from colorthief import ColorThief
from PIL import Image

BASE = 'https://stodevx.github.io/sga-weekly-movies'


def dedupe(lst, *, key):
    """dedupe([{'w': 1}], key=lambda x: x['w'])"""
    seen = set()
    for item in lst:
        if key(item) not in seen:
            yield item
        seen.add(key(item))


def now():
    return datetime.now(tz=pytz.timezone('America/Winnipeg'))


def json_serialize(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def load_movie_info(folder):
    movie_file = folder / 'movie.json'
    with movie_file.open('r', encoding='utf-8') as infile:
        movie = json.load(infile)

    del movie["Metascore"]
    del movie["imdbRating"]
    del movie["imdbVotes"]
    del movie["Poster"]
    del movie["Response"]
    movie['ReleaseDate'] = datetime.strptime(movie['Released'], '%d %b %Y').date()
    movie['Genres'] = movie['Genre'].split(', ') if 'Genre' in movie else []

    return movie


def load_showings_as_isoformat(folder):
    showings_file = folder / 'showings.json'
    with showings_file.open('r', encoding='utf-8') as infile:
        showings = json.load(infile)

    offset = now().strftime('%z')
    for day in showings['showings']:
        for time in day['times']:
            ds = f"{day['date']} {time}{offset}"
            yield {
                'time': datetime.strptime(ds, '%Y-%m-%d %H:%M%z'),
                'location': day['location'],
            }


def find_posters(folder, url_root):
    folder = folder / 'poster'
    for f in folder.iterdir():
        if f.suffix not in ('.jpg', '.png'):
            continue

        with Image.open(f) as img:
            width, height = img.size

        yield {
            'url': f'{url_root}/poster/{f.name}',
            'filename': f'poster/{f.name}',
            'width': width,
            'height': height,
        }


def index_trailer_thumbnails(movie_folder, trailer_key, url_root):
    trailer_folder = movie_folder / 'trailers' / trailer_key
    for f in trailer_folder.iterdir():
        if f.suffix not in ('.jpg', '.png'):
            continue

        with Image.open(f) as img:
            width, height = img.size

        yield {
            'url': f'{url_root}/trailers/{trailer_key}/{f.name}',
            'filename': f'trailers/{trailer_key}/{f.name}',
            'width': width,
            'height': height,
        }


def process_trailer(folder, trailer, url_root):
    print(f'trailer {trailer["url"]}', file=sys.stderr)
    thumbnails_gen = index_trailer_thumbnails(folder, trailer['key'], url_root)
    deduped_thumbs = dedupe(thumbnails_gen, key=lambda x: x['width'])
    thumbnails = sorted(deduped_thumbs, key=lambda x: x['width'])

    del trailer['site']
    del trailer['size']
    del trailer['key']

    trailer['lang'] = f"{trailer['iso_639_1']}-{trailer['iso_3166_1']}"
    del trailer['iso_639_1']
    del trailer['iso_3166_1']

    trailer['thumbnails'] = thumbnails
    trailer['colors'] = find_trailer_colors(folder, thumbnails)

    return trailer


def find_trailers(folder, url_root):
    trailers_file = folder / 'trailers.json'
    with trailers_file.open('r', encoding='utf-8') as infile:
        trailer_info = json.load(infile)

    for trailer in trailer_info['trailers']:
        yield process_trailer(folder, trailer, url_root)


def find_colors(file):
    colors = ColorThief(file.as_posix())
    return {
        'dominant': colors.get_color(quality=1),
        'palette': colors.get_palette(color_count=6),
    }


def find_trailer_colors(folder, thumbs):
    smallest = min(thumbs, key=lambda p: p['width'])
    return find_colors(folder / smallest['filename'])


def find_poster_colors(folder, posters):
    smallest = min(posters, key=lambda p: p['width'])
    return find_colors(folder / smallest['filename'])


def process_movie(folder):
    folder = pathlib.Path(folder)

    print(f'processing {folder!r}', file=sys.stderr, flush=True)

    url_root = f'{BASE}/movies/{urllib.parse.quote(folder.name)}'

    movie = load_movie_info(folder)
    posters_iter = find_posters(folder, url_root)
    deduped_posters = dedupe(posters_iter, key=lambda p: p['width'])
    all_posters = sorted(deduped_posters, key=lambda p: p['width'])
    all_trailers = list(find_trailers(folder, url_root))

    data = {
        'root': url_root,
        'info': movie,
        'showings': list(load_showings_as_isoformat(folder)),
        'poster': {
            'sizes': all_posters,
            'colors': find_poster_colors(folder, all_posters),
        },
        'trailers': all_trailers,
    }

    index = folder / 'index.json'
    with index.open('w', encoding='utf-8') as outfile:
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)

    return data


def save_archive(entries):
    ordered = sorted(entries, key=lambda m: m['root'])

    with open('archive.json', 'w', encoding='utf-8') as outfile:
        data = {'movies': [f'{m["root"]}/index.json' for m in ordered]}
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)


def save_latest(entries):
    last = max(entries, key=lambda m: m['root'])
    last_showing = max(s['time'] for s in last['showings'])
    last_showing_date = last_showing.isoformat().split('T')[0]

    with open('next.json', 'w', encoding='utf-8') as outfile:
        data = {
            'movie': f'{last["root"]}/index.json',
            'last_showing': last_showing_date,
        }
        json.dump(data, outfile, default=json_serialize, ensure_ascii=False)


def main():
    entries = []
    root_dir = pathlib.Path('./movies')

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
        futures = [
            pool.submit(process_movie, folder.as_posix())
            for folder in root_dir.iterdir()
            if folder.is_dir()
        ]

        for future in as_completed(futures):
            try:
                data = future.result()
                entries.append(data)
            except Exception as exc:
                raise exc

    save_archive(entries)
    save_latest(entries)


if __name__ == '__main__':
    main()
