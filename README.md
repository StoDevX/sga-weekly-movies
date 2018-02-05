# sga-weekly-movies
An archive of the SGA weekly movies

## What?
This repository maintains a list of the movies shown by the Student Government Association at St. Olaf College, who choose a new movie to show on campus each week.

We began tracking these movies in the fall of the 2017-18 school year.

## Usage
If you want to do things with the raw data, you're free to use `master`.

However, we process the data to do things like extract the dominant color of the movie poster; those processed files are stored on the `gh-pages` branch.

If you're wanting to use the processed data files, here's what you need to know:

- There are two top-level files, `archive.json` and `next.json`. They are more-or-less just pointers to the actual data files.
- Each movie has an `index.json` file that actually contains the data

These `index.json` files look like this:

```json
{
  "root": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation",
  "info": {
    "Title": "Annabelle: Creation",
    "Year": "2017",
    "Rated": "R",
    "Released": "11 Aug 2017",
    "Runtime": "109 min",
    "Genres": ["Horror", "Mystery", "Thriller"],
    "Genre": "Horror, Mystery, Thriller",
    "Director": "David F. Sandberg",
    "Writer": "Gary Dauberman, Gary Dauberman (based on characters created by)",
    "Actors": "Anthony LaPaglia, Samara Lee, Miranda Otto, Brad Greenquist",
    "Plot": "12 years after the tragic death of their little girl, a dollmaker and his wife welcome a nun and several girls from a shuttered orphanage into their home, where they soon become the target of the dollmaker's possessed creation, Annabelle.",
    "Language": "English, Spanish",
    "Country": "USA",
    "Awards": "1 nomination.",
    "Ratings": [
      { "Source": "Internet Movie Database", "Value": "6.7/10" },
      { "Source": "Rotten Tomatoes", "Value": "70%" },
      { "Source": "Metacritic", "Value": "62/100" }
    ],
    "imdbID": "tt5140878",
    "Type": "movie",
    "DVD": "24 Oct 2017",
    "BoxOffice": "$101,788,793",
    "Production": "New Line Cinema",
    "Website": "http://www.annabellemovie.com",
    "ReleaseDate": "2017-08-11"
  },
  "showings": [
    { "time": "2017-10-28T17:00:00-06:00", "location": "Viking Theater" },
    { "time": "2017-10-28T19:30:00-06:00", "location": "Viking Theater" },
    { "time": "2017-10-28T22:00:00-06:00", "location": "Viking Theater" }
  ],
  "poster": {
      "sizes": [
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/96.jpg",
          "filename": "poster/96.jpg",
          "width": 96,
          "height": 142
        },
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/192.jpg",
          "filename": "poster/192.jpg",
          "width": 192,
          "height": 285
        },
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/300.jpg",
          "filename": "poster/300.jpg",
          "width": 300,
          "height": 445
        },
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/512.jpg",
          "filename": "poster/512.jpg",
          "width": 512,
          "height": 759
        },
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/768.jpg",
          "filename": "poster/768.jpg",
          "width": 768,
          "height": 1138
        },
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/poster/1024.jpg",
          "filename": "poster/1024.jpg",
          "width": 1024,
          "height": 1517
        }
      ],
      "colors": {
        "dominant": [ 23, 41, 45 ],
        "palette": [
          [ 21, 39, 42 ],
          [ 186, 202, 199 ],
          [ 86, 116, 126 ],
          [ 125, 163, 177 ],
          [ 108, 143, 161 ],
          [ 60, 90, 101 ]
        ]
      },
  }
  "trailers": [
    {
      "name": "Announcement Tease",
      "type": "Teaser",
      "url": "https://www.youtube.com/watch?v=OUDXAOXBxa4",
      "lang": "en-US",
      "colors": {
        "dominant": [ 23, 41, 45 ],
        "palette": [
          [ 21, 39, 42 ],
          [ 186, 202, 199 ],
          [ 86, 116, 126 ],
          [ 125, 163, 177 ],
          [ 108, 143, 161 ],
          [ 60, 90, 101 ]
        ]
      },
      "thumbnails": [
        {
          "url": "https://stodevx.github.io/sga-weekly-movies/movies/2017-10-28%20Annabelle%20Creation/trailers/OUDXAOXBxa4/mq.jpg",
          "filename": "trailers/OUDXAOXBxa4/mq.jpg",
          "width": 320,
          "height": 180
        },
        // ...
      ]
    },
    // ...
  ]
}
```

A few things to note:

- Inside the `posters` object, you get a selection of poster sizes, as well as a mapping of the poster colors
- Similarly, each trailer comes with a selection of thumbnails and the dominant colors of that trailer

## Contibuting
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
