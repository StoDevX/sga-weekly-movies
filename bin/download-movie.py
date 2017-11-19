#!/usr/bin/env python3

import os
import sys
import json
import argparse

import requests
from pick import pick


API_KEY = os.getenv('OMDB_API_KEY', None)

if not API_KEY:
    print(f'This tool requires an OMDB api key. If you do not have one, please visit <http://www.omdbapi.com/apikey.aspx>, then `export OMDB_API_KEY="your-key" pipenv run python {sys.argv[0]}`', file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description='Download movie info.')
    parser.add_argument('date', metavar='SHOW_DATE',
                        help='the first date shown at Olaf, in YYYY-MM-DD')
    parser.add_argument('title', metavar='TITLE',
                        help='the movie title to fetch')
    parser.add_argument('--year', default=None, help='the year the movie was released')

    args = parser.parse_args()
    # args.date = args.date.replace('/', '-')

    return args


def get_movie(imdbID):
    params = {'i': imdbID, 'apiKey': API_KEY, 'plot': 'short'}
    r = requests.get('http://www.omdbapi.com/', params=params)
    results = r.json()
    return results


def find_movie(title, year):
    params = {'s': title, 'apiKey': API_KEY, 'type': 'movie'}
    if year:
        params['y'] = year
    r = requests.get('http://www.omdbapi.com/', params=params)
    results = r.json()
    options = [f'{m["Title"]} ({m["Year"]}) <{m["Poster"]}>' for m in results['Search']]
    [_, chosen_index] = pick(options)

    chosen_movie = results['Search'][chosen_index]

    return get_movie(chosen_movie['imdbID'])


def main():
    args = parse_args()

    movie = find_movie(args.title, args.year)

    movie_dir = os.path.join('movies', f'{args.date} {args.title}')
    os.makedirs(movie_dir, exist_ok=True)
    with open(os.path.join(movie_dir, 'movie.json'), 'w', encoding='utf-8') as outfile:
        json.dump(movie, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')
    with open(os.path.join(movie_dir, 'showings.json'), 'w', encoding='utf-8') as outfile:
        showings = {
            'showings': [
                {
                    'date': args.date.replace('-', '/'),
                    'times': ['17:00', '19:30', '22:00'],
                    'location': 'Viking Theater',
                },
            ]
        }
        json.dump(showings, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

if __name__ == '__main__':
    main()
