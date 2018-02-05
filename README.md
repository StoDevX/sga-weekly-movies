# sga-weekly-movies
An archive of the SGA weekly movies

To add a new movie:

1. Get an OMDB API key: http://www.omdbapi.com/apikey.aspx
2. Take the key they email you, and export it: `export OMDB_API_KEY="my-key"`
    - I recommend putting this in your shell's config file (`~/.bashrc`, `~/.config/fish/config.fish`, etc)
3. Install Pipenv, if you don't have it already: https://docs.pipenv.org
4. Install our dependencies: `pipenv install`
5. Download the movie info: `./bin/add-movie YYYY-MM-DD MovieName`
    - `YYYY-MM-DD` is the date that the movie will be shown
    - `MovieName` is the name of the movie
    - The script will ask you to pick the correct movie
6. Make sure the "showings" are correct (in `showings.json`) – sometimes SGA shows movies on odd days/times
7. Commit and PR!

---

If you need to check that your files are workable, you can run

```bash
pipenv run python bin/build.py
```
