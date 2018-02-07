import requests
import sys
from pathlib import Path
from PIL import Image
from .download_file import download_file
from .keys import TMDB_API_KEY

youtube_sizes = {
    "small": "default",
    "hq": "hqdefault",
    "mq": "mqdefault",
    "lq": "sddefault",
    "full": "maxresdefault",
}

youtube_dimensions = {
    "small": (120, 90),
    "hq": (480, 360),
    "mq": (320, 180),
    "lq": (640, 480),
    "full": (1280, 720),
}

non_letterboxed_yt_thumbs = ['full', 'mq']


def resize_thumbnail(*, src: str, dest: str, size: str):
    img = Image.open(src)
    before_width, before_height = img.size
    img.thumbnail(size=youtube_dimensions[size], resample=Image.LANCZOS)
    after_width, after_height = img.size
    if after_width != before_width and after_height != before_height:
        img.save(dest)


def ytimg(video_id: str, size: str):
    return f'https://i.ytimg.com/vi/{video_id}/{size}.jpg'


def download_youtube_thumbnail(trailer_id: str, trailer_size: str, dest_folder: Path):
    dest_path = dest_folder / f'{trailer_size}.jpg'

    if dest_path.is_file():
        print(f'skipping trailer {trailer_size}.jpg because it exists')
        return

    print(f'downloading {trailer_size}.jpg')
    url = ytimg(trailer_id, youtube_sizes[trailer_size])

    download_file(url, dest_path)


def download_hq_youtube_thumbnail(trailer_id: str, dest_folder: Path):
    # we want to try the non-letterboxed thumbnails first,
    # and then fall back to the letterboxed ones
    all_sizes = list(youtube_sizes.keys())
    all_sizes.sort(key=lambda s: youtube_dimensions[s][0], reverse=True)
    sizes = non_letterboxed_yt_thumbs + all_sizes

    for size in sizes:
        r = requests.head(ytimg(trailer_id, youtube_sizes[size]))
        print(r)
        if not (200 <= r.status_code < 300):
            print(f'the {size} thumbnail was unavailable')
            continue

        print(f'using the {size} thumbnail')
        download_youtube_thumbnail(trailer_id, size, dest_folder)
        return size

    print(f'no thumbnails were found for {trailer_id}')
    return None


def download_trailer(trailer_info, dest_folder: Path):
    trailer_id = trailer_info['key']

    print(f'downloading trailer {trailer_id} - "{trailer_info["name"]}"')

    dest_folder = dest_folder / trailer_id
    dest_folder.mkdir(exist_ok=True, parents=True)

    if trailer_info['site'] == 'YouTube':
        largest_size = download_hq_youtube_thumbnail(trailer_id, dest_folder)
        if largest_size is None:
            return
        for size in (set(youtube_sizes) - {largest_size}):
            print(f'generating {size} from {largest_size}')
            resize_thumbnail(src=dest_folder / f'{largest_size}.jpg',
                             dest=dest_folder / f'{size}.jpg',
                             size=size)
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
