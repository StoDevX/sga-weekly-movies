#!/usr/bin/env python3

import sys
import json
from pathlib import Path

from lib.movies import get_movie
from lib.posters import download_posters
from lib.trailers import get_trailers, download_trailer


def update_movie_info(movie, movie_dir: Path):
    movie = get_movie(movie['imdbID'])
    trailers = list(get_trailers(movie['imdbID']))

    download_posters(movie, movie_dir)

    trailers_file = movie_dir / 'trailers.json'
    with open(trailers_file, 'w', encoding='utf-8') as outfile:
        json.dump({'trailers': trailers}, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    for trailer in trailers:
        download_trailer(trailer, movie_dir / 'trailers')


def main(movie_info_files):
    for filepath in movie_info_files:
        movie_dir = filepath.parent
        print(movie_dir)
        with open(filepath, 'r', encoding='utf-8') as infile:
            movie_info = json.load(infile)
        update_movie_info(movie_info, movie_dir)


if __name__ == '__main__':
    current = Path(__file__).parent.parent / 'movies'
    main(sys.argv[1:] or current.glob('*/movie.json'))
