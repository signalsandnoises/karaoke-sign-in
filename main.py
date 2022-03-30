# INSTRUCTIONS: include your lastFM API token and username in config.ini, then run this script
# This script will use lastfm_query.py to query your last.fm data, and write artists.csv
# This script will then read artists.csv, query the karaoke place for each artist, and write songs.tsv 

import os
import sys
import lastfm_query
import requests
from db import DB
from colorama import init as colorinit
from colorama import Fore, Style

SONG_LANGUAGE = "english"
OUTPUT_DIR = "output"

## Init cross-platform color output support
colorinit()

## Create output directory if needed
if (not os.path.exists(OUTPUT_DIR)):
    os.mkdir(OUTPUT_DIR)

## Query last.fm and write arists.csv, but only if it does not already exist
if (not os.path.exists(os.path.join(OUTPUT_DIR, "artists.csv"))):
    print(f"{Style.DIM}Getting artists from last.fm...")
    artist_names = lastfm_query.scrapeArtists()
    with open(os.path.join(OUTPUT_DIR, "artists.csv"), "w", encoding="utf-8") as artist_file:
        artist_file.writelines(artist_names)

## Load artists.csv into artists
artist_file = open(os.path.join(OUTPUT_DIR, "artists.csv"), "r", encoding="utf-8")
artists = [artist[:-1] for artist in artist_file.readlines()]
artist_file.close()

## Fetch all available songs from HealSonic
print(f"\n{Style.DIM}Fetching all available songs from HealSonic...{Style.RESET_ALL}", end="")
query = f"https://search.healsonic.com/assets/php/search.php?kw=&lang={SONG_LANGUAGE.title()}"
res = requests.get(query)
if (res.status_code != 200):
    sys.exit("Query to HealSonic Karaoke was not completed successfully")
data = res.json()

## Populate in-memory database with available songs
db = DB()
try: 
    print(f"{Style.DIM}Populating in-memory database with available songs...{Style.RESET_ALL} ", end="")
    db.populate(data)
    print("Done", end="\n")
except Exception as e:
    print(e)
    sys.exit('Error: database population failed')

## Iterate through the artists, query the in-memory karaoke database, and write to songs_file
song_count = 0
songs_file = open(os.path.join(OUTPUT_DIR, "songs.tsv"), "w", encoding="utf-8")
songs_file.write("ARTIST\tSONG\tCODE\tVERSION\n")
for i, artist in enumerate(artists):
    current_songs = db.search_artist(artist)
    for song in current_songs:
        songs_file.write(f'{song[3]}\t{song[2]}\t{song[0]}\t{song[1]}\n')
        song_count += 1
    if (len(current_songs) > 0):
        print(f"\r{Fore.CYAN}** {Fore.YELLOW}{len(current_songs)} songs found for {artist: <10}", sep=' ', end='\n', flush=True)
    else:
        print(f"\r{Style.DIM}Searching artist {i+1} of {len(artists)}{Style.RESET_ALL}", sep=' ', end='', flush=True)
print(f'\r{Fore.GREEN}{"Search complete.": <30}\n', sep=' ', end='\n', flush=True)
if song_count > 0:
    print(f'{Fore.GREEN}SUCCESS: {Fore.YELLOW}Found {song_count} {"song" if song_count == 1 else "songs"} from your Last.FM artist(s)')
    print(f'{Fore.BLUE}Songs file: {os.path.realpath(songs_file.name)}')
else:
    print(f'{Fore.RED}No songs found from your Last.FM artists')
print(Style.RESET_ALL)
songs_file.close()
