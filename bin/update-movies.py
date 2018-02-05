#!/usr/bin/env python3

import os
import sys
import json
import glob

from lib import get_movie, get_trailers, download_posters, download_trailer


def update_movie_info(movie, movie_dir):
    movie = get_movie(movie['imdbID'])
    trailers = list(get_trailers(movie['imdbID']))

    movie_file = os.path.join(movie_dir, 'movie.json')
    download_posters(movie, movie_dir)

    trailers_file = os.path.join(movie_dir, 'trailers.json')
    with open(trailers_file, 'w', encoding='utf-8') as outfile:
        json.dump({'trailers': trailers}, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    for trailer in trailers:
        download_trailer(trailer, os.path.join(movie_dir, 'trailers'))

    # with open(os.path.join(movie_dir, 'showings.json'), 'r', encoding='utf-8') as infile:
    #     showings = json.load(infile)
    # for showing in showings['showings']:
    #     if '/' in showing['date']:
    #         showing['date'] = showing['date'].replace('/', '-')
    # with open(os.path.join(movie_dir, 'showings.json'), 'w', encoding='utf-8') as outfile:
    #     json.dump(showings, outfile)


def main(movie_info_files):
    for filepath in movie_info_files:
        movie_dir = os.path.dirname(filepath)
        print(movie_dir)
        with open(filepath, 'r', encoding='utf-8') as infile:
            movie_info = json.load(infile)
        update_movie_info(movie_info, movie_dir)


if __name__ == '__main__':
    main(sys.argv[1:] or glob.glob('./movies/*/movie.json'))
