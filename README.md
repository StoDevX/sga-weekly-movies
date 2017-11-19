# sga-weekly-movies
An archive of the SGA weekly movies

My goal is (as automatically as possible, ofc) to input a movie title/year, the days and times of the showing, and fetch both the info json _and_ to download the poster into the repo, so that we don't abuse the image hosts.

For now, I'm adding these manually – I'll eventually subscribe to <http://www.omdbapi.com> for the automation / because I feel guilty manually scraping them.

---

If you create a movie folder and add "movie.json" to it, you can just run

```bash
pipenv run python bin/download-posters.py
```

which will go download any posters that aren't already downloaded.

If you don't have Pipenv installed, you'll need to install [Pipenv](https://docs.pipenv.org), then `pipenv install` in this repository folder.

---

To check that your files are workable, you can run

```bash
pipenv run python bin/build.py
```

---

The movie folders are named according to the following pattern:

```
$YEAR-$MONTH-$DAY $NAME
```

where MONTH-DAY is the first day that the movie is playing.

All days that the movie plays should be recorded in the "showings.json" file, as well as the times that it plays.
