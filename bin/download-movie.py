#!/usr/bin/env python3

import argparse
from datetime import datetime
from lib import get_movie


def main():
    parser = argparse.ArgumentParser(description='Download movie info.')
    parser.add_argument('date', metavar='SHOW_DATE',
                        help='the first date shown at Olaf, in YYYY-MM-DD')
    parser.add_argument('title', metavar='TITLE',
                        help='the movie title to fetch')
    parser.add_argument('--year', default=None, help='the year the movie was released')

    args = parser.parse_args()

    args.date = datetime.strptime(args.date, '%Y-%m-%d').date()

    get_movie(title=args['title'], date=args['date'], year=args['year'])


if __name__ == '__main__':
    main()
