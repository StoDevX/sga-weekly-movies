#!/usr/bin/env python3

import glob
import json
import sys
import os

from lib import download_trailer


def main(trailer_files):
    for filepath in trailer_files:
        print(filepath)

        with open(filepath, 'r', encoding='utf-8') as infile:
            trailer_list = json.load(infile)

        dest_folder = os.path.join(os.path.dirname(filepath), 'trailers')

        for trailer_info in trailer_list['trailers']:
            download_trailer(trailer_info, dest_folder)


if __name__ == '__main__':
    main(sys.argv[1:] or glob.glob('./movies/*/trailers.json'))
