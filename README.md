# Wikiplot

##Introduction

Scraps the plot of the movie given by the user from its Wikipedia page and stores it in an epub to be read later in your e-reading device!

##Usage

From the main directory,

```sh
$ python wikiplot.py [OPTION] MOVIENAME 
```

##Options

```sh
  -h, --help  show this help message and exit
  -n, --new   Store the plot in a new epub file
  -a, --app   Append to an existing epub file
```

##Note

* To append to an existing file, the `.epub` file must be placed in the `epubs/` directory.
* Appending actually creates a new `.epub` file with essential contents copied from the old file with some edits and additions for the new movie.
* The new `.epub` file is created in the `epubs/` folder.