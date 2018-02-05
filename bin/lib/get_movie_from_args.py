import json
from datetime import timedelta
from pathlib import Path
from .download_trailer import download_trailer
from .trailers import get_trailers
from .download_posters import download_posters
from .movies import find_movie


def get_movie(args):
    movie = find_movie(args.title, args.year)
    if not movie:
        return

    trailers = list(get_trailers(movie['imdbID']))

    movie_dir = Path(__file__).parent.parent / 'movies' / f'{args.date.isoformat()} {args.title}'
    movie_dir.mkdir(parents=True, exist_ok=True)

    movie_file = movie_dir / 'movie.json'
    with open(movie_file, 'w', encoding='utf-8') as outfile:
        json.dump(movie, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    download_posters(movie, movie_dir)

    trailers_file = movie_dir / 'trailers.json'
    with open(trailers_file, 'w', encoding='utf-8') as outfile:
        json.dump({'trailers': trailers}, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')

    for trailer in trailers:
        download_trailer(trailer, movie_dir / 'trailers')

    showings_file = movie_dir / 'showings.json'
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
