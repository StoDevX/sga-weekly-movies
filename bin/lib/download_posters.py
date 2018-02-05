import re
import os
from pathlib import Path
from .download_file import download_file

sizes = [
    96,
    96 * 2,
    300,
    512,
    768,
    1024,
]


def download_posters(movie_info, dest_dir: Path):
    url = re.sub(r'_SX300\.jpg$', '_SX$1.jpg', movie_info['Poster'])

    poster_dir = dest_dir / 'poster'
    poster_dir.mkdir(exist_ok=True, parents=True)

    for size in sizes:
        dest_path = poster_dir / f'{size}.jpg'
        if os.path.isfile(dest_path):
            print(f'skipping poster/{size}.jpg because it exists')
            continue

        print(f'downloading poster/{size}.jpg')
        poster_url = url.replace('$1', str(size))

        download_file(poster_url, dest_path)
