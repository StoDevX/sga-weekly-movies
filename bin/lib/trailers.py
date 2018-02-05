import requests
import sys
from pathlib import Path
from .download_file import download_file
from .keys import TMDB_API_KEY

youtube_sizes = {
    "small": "default",
    "hq": "hqdefault",
    "mq": "mqdefault",
    "lq": "sddefault",
    "full": "maxresdefault",
}


def download_youtube_thumbnail(trailer_id: str, trailer_size: str, dest_folder: Path):
    dest_path = dest_folder / f'{trailer_size}.jpg'

    if dest_path.is_file():
        print(f'skipping trailer {trailer_size}.jpg because it exists')
        return

    print(f'downloading {trailer_size}.jpg')
    url = f'https://img.youtube.com/vi/{trailer_id}/{youtube_sizes[trailer_size]}.jpg'

    download_file(url, dest_path)


def download_trailer(trailer_info, dest_folder: Path):
    trailer_id = trailer_info['key']

    print(f'downloading trailer {trailer_id} - "{trailer_info["name"]}"')

    dest_folder = dest_folder / trailer_id
    dest_folder.mkdir(exist_ok=True, parents=True)

    if trailer_info['site'] == 'YouTube':
        for size in youtube_sizes:
            download_youtube_thumbnail(trailer_id, size, dest_folder)
    else:
        print(f'Unknown trailer site "{trailer_info["site"]}"; skipping thumbnail download', file=sys.stderr)


def get_trailers(imdb_id):
    params = {'language': 'en-US', 'api_key': TMDB_API_KEY}
    url = f'https://api.themoviedb.org/3/movie/{imdb_id}/videos'
    r = requests.get(url, params=params)

    data = r.json()

    if 'status_message' in data:
        if data['status_code'] is 34:
            print(f'The IMDB ID {imdb_id} was not present in TMDB\'s db. Continuing without trailers.',
                  file=sys.stderr)
            return []
        else:
            print('TMDB API error:', file=sys.stderr)
            print(data['status_message'], file=sys.stderr)
            sys.exit(1)

    if 'results' not in data:
        print('No trailers found! Continuing without them.', file=sys.stderr)
        return []

    for trailer in data['results']:
        del trailer['id']
        if trailer['site'] == 'YouTube':
            trailer['url'] = f'https://www.youtube.com/watch?v={trailer["key"]}'
        else:
            trailer['url'] = None
        yield trailer
