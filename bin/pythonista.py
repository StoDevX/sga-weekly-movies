#!/usr/bin/env python3

import sys
import dialogs
from datetime import date, timedelta
from lib import get_movie


def main():
    today = date.today()
    friday = today + timedelta((4 - today.weekday()) % 7)

    args = dialogs.form_dialog(title="Movie", fields=[
        {
            'type': 'text',
            'key': 'title',
            'title': 'Movie Title',
            'placeholder': 'What\'s the movie?',
        },
        {
            'type': 'date',
            'key': 'date',
            'title': 'First day of movie',
            'value': friday,
        },
    ])

    if not args:
        sys.exit(0)

    args['date'] = args['date'].date()

    get_movie(title=args['title'], date=args['date'], year=None)

    print('done!')


if __name__ == '__main__':
    main()
