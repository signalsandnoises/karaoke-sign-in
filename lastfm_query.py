## This script reads config.ini, queries the last.fm API for that user's library, and saves the artists in a text file
## labeled "artists.csv". One artist per name. No playcount information is recorded, though artists are sorted by
## decreasing playcount.

import os.path
import configparser
import requests
from time import sleep
from colorama import Fore, Style

## Read the config file
configParser = configparser.RawConfigParser()
configParser.read(os.path.join("config", "config.ini"))
lastFM_key = configParser["lastFM"]["key"]
lastFM_username = configParser["lastFM"]["username"]

## Query the number of pages for the configured user
url = f"https://ws.audioscrobbler.com/2.0/?method=library.getartists&api_key={lastFM_key}&user={lastFM_username}&format=json&limit=1000"
res = requests.get(url)
if (res.status_code != 200):
    raise ConnectionError("Could not connect to last.fm API")
totalPages = int(res.json()['artists']['@attr']['totalPages'])


## Iterate through pages, scraping the artists IN ORDER (by decreasing playcount)
## This makes a call to the last.fm API for each page of 50 artists.
def scrapeArtists():
    artist_names = []
    for page in range(1, totalPages+1):
        res = requests.get(f"{url}&page={page}")
        if (res.status_code != 200):
            raise ConnectionError(f"Could not connect to last.fm API for page {page}")
        artists = res.json()['artists']['artist'] # a list
        artist_names += [artist["name"] + "\n" for artist in artists]
        print(f"\r{Style.DIM}Page {page} of {totalPages}{Style.RESET_ALL}", sep=' ', end='', flush=True)
        sleep(1)

    return artist_names


if (__name__ == "__main__"):
    scrapeArtists()
