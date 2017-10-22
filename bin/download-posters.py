#!/usr/bin/env python3
import glob
import json
import sys
import re
import os

import requests

sizes = [
    96,
    96 * 2,
    300,
    512,
    768,
    1024,
]


def main(movie_info_files):
    for filepath in movie_info_files:
        print(filepath)
        with open(filepath, 'r', encoding='utf-8') as infile:
            movie_info = json.load(infile)

        url = re.sub(r'_SX300\.jpg$', '_SX$1.jpg', movie_info['Poster'])

        for size in sizes:
            dest_path = filepath.replace('movie.json', f'poster-{size}.jpg')
            if os.path.isfile(dest_path):
                print(f'skipping poster-{size}.jpg because it exists')
                continue

            print(f'downloading poster-{size}.jpg')
            poster_url = url.replace('$1', str(size))

            r = requests.get(poster_url, stream=True)
            with open(dest_path, 'wb') as outfile:
                for chunk in r.iter_content(chunk_size=128):
                    outfile.write(chunk)


if __name__ == '__main__':
    main(sys.argv[1:] or glob.glob('./movies/*/movie.json'))
