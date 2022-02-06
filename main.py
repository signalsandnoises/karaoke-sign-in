# INSTRUCTIONS: include your lastFM API token and username in config.txt, then run this script
# This script will use lastfm_query.py to query your last.fm data, and write artists.csv
# This script will then read artists.csv, query the karaoke place for each artist, and write songs.tsv

import os.path
import karaoke_query
import lastfm_query
import random
from time import sleep

AVERAGE_QUERY_DELAY = 0.3
AVERAGE_QUERY_RATE = 1/AVERAGE_QUERY_DELAY

if (not os.path.exists("artists.csv")):
    print("Getting artists from last.fm...")
    lastfm_query.scrapeArtists()
    print("Got all the artists from last.fm.\n")

artist_file = open("artists.csv", "r", encoding="utf-8")
artists = [artist[:-1] for artist in artist_file.readlines()]
artist_file.close()

songs = []
songs_file = open("songs.tsv", "w", encoding="utf-8")
songs_file.write("ARTIST\tSONG\tCODE\tVERSION\n")
for i, artist in enumerate(artists[0:15]):
    current_songs = karaoke_query.getKaraokeSongs(artist)
    for song in current_songs:
        songs_file.write('\t'.join(song) + '\n')
    if (len(current_songs) > 0):
        print(f"{i}/{len(artists)} {len(current_songs)} songs found for {artist}")
    else:
        print(f"{i}/{len(artists)}")
    period = random.expovariate(AVERAGE_QUERY_RATE)
    sleep(period)
songs_file.close()
