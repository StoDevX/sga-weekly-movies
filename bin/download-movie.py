#!/usr/bin/env python3

import os
import re
import sys
import json
import argparse
from datetime import datetime, timedelta

from lib import find_movie, get_trailers


OMDB_API_KEY = os.getenv('OMDB_API_KEY', None)
TMDB_API_KEY = os.getenv('TMDB_API_KEY', None)

if not OMDB_API_KEY:
    print(f'This tool requires an OMDB api key. If you do not have one, please visit <http://www.omdbapi.com/apikey.aspx>, then `export OMDB_API_KEY="your-key" pipenv run python {sys.argv[0]}`', file=sys.stderr)

if not TMDB_API_KEY:
    print(f'This tool requires a TMDB api key. If you do not have one, please visit <https://www.themoviedb.org>, log in and get the v3 API key, then `export TMDB_API_KEY="your-key" pipenv run python {sys.argv[0]}`', file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(description='Download movie info.')
    parser.add_argument('date', metavar='SHOW_DATE',
                        help='the first date shown at Olaf, in YYYY-MM-DD')
    parser.add_argument('title', metavar='TITLE',
                        help='the movie title to fetch')
    parser.add_argument('--year', default=None, help='the year the movie was released')

    args = parser.parse_args()
    args.date = datetime.strptime(args.date, '%Y-%m-%d')
    args.date = args.date.date()

    return args


def main():
    args = parse_args()

    movie = find_movie(args.title, args.year)
    trailers = list(get_trailers(movie['imdbID']))

    movie_dir = os.path.join('movies', f'{args.date.isoformat()} {args.title}')
    os.makedirs(movie_dir, exist_ok=True)

    movie_file = os.path.join(movie_dir, 'movie.json')
    with open(movie_file, 'w', encoding='utf-8') as outfile:
        json.dump(movie, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    download_posters(movie, movie_dir)

    trailers_file = os.path.join(movie_dir, 'trailers.json')
    with open(trailers_file, 'w', encoding='utf-8') as outfile:
        json.dump({'trailers': trailers}, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    for trailer in trailers:
        download_trailer(trailer, os.path.join(movie_dir, 'trailers'))

    showings_file = os.path.join(movie_dir, 'showings.json')
    with open(showings_file, 'w', encoding='utf-8') as outfile:
        showings = {
            'showings': [
                {
                    'date': args.date.isoformat(),
                    'times': ['17:00', '19:30', '22:00'],
                    'location': 'Viking Theater',
                },
                {
                    'date': (args.date + timedelta(days=1)).isoformat(),
                    'times': ['17:00', '19:30', '22:00'],
                    'location': 'Viking Theater',
                },
            ]
        }
        json.dump(showings, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

if __name__ == '__main__':
    main()
