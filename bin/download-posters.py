#!/usr/bin/env python3

import glob
import json
import sys
import os

from lib import download_posters


def main(movie_info_files):
    for filepath in movie_info_files:
        print(filepath)
        with open(filepath, 'r', encoding='utf-8') as infile:
            movie_info = json.load(infile)

        dest_dir = os.path.dirname(filepath)
        download_posters(movie_info, dest_dir)


if __name__ == '__main__':
    main(sys.argv[1:] or glob.glob('./movies/*/movie.json'))
