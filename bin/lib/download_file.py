import requests


def download_file(url, dest_path):
    r = requests.get(url, stream=True)

    with open(dest_path, 'wb') as outfile:
        for chunk in r.iter_content(chunk_size=128):
            outfile.write(chunk)
