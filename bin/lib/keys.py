import os
import sys


OMDB_API_KEY = os.getenv('OMDB_API_KEY', None)
if not OMDB_API_KEY:
    print(f'This tool requires an OMDB api key. If you do not have one, please visit <http://www.omdbapi.com/apikey.aspx>, then `export OMDB_API_KEY="your-key" pipenv run python {sys.argv[0]}`', file=sys.stderr)


TMDB_API_KEY = os.getenv('TMDB_API_KEY', None)
if not TMDB_API_KEY:
    print(f'This tool requires a TMDB api key. If you do not have one, please visit <https://www.themoviedb.org>, log in and get the v3 API key, then `export TMDB_API_KEY="your-key" pipenv run python {sys.argv[0]}`', file=sys.stderr)
