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
        {
            'type': 'switch',
            'key': 'one_day_only',
            'title': 'Only shown for one day?',
            'value': False
        },
        {
            'type': 'switch',
            'key': 'exact',
            'title': 'Skip search; use exact?',
            'value': False
        }
    ])

    if not args:
        sys.exit(0)

    args['date'] = args['date'].date()

    get_movie(title=args['title'], date=args['date'], year=None, one_day=args['one_day_only'], exact_match=args['exact'])

    print('done!')


if __name__ == '__main__':
    main()
