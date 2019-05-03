import json
from datetime import timedelta
from pathlib import Path
from .trailers import get_trailers, download_trailer
from .posters import download_posters
from .movies import search_for_movie


def get_movie(*, title, year, date, one_day, exact_match):
    movie = search_for_movie(title, year, exact_match)
    if not movie:
        return

    trailers = list(get_trailers(movie['imdbID']))

    movie_dest_dirname = movie["Title"].replace('/', ':')
    movie_dir = Path(__file__).parent.parent.parent / 'movies' / f'{date.isoformat()} {movie_dest_dirname}'
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
        
    showings = {'showings': []}
    day_count = 1 if one_day else 2

    for n in range(day_count):
        a_date = date + timedelta(days=n)
        showings['showings'].append(
            {
                'date': a_date.isoformat(),
                'times': ['17:00', '19:30', '22:00'],
                'location': 'Viking Theater',
            }
        )
    
    print(showings)

    showings_file = movie_dir / 'showings.json'
    with open(showings_file, 'w', encoding='utf-8') as outfile:
        json.dump(showings, outfile, ensure_ascii=False, indent=2)
        outfile.write('\n')
