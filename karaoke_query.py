## This file defines functions to query the karaoke database

import requests
import urllib.parse
from fuzzywuzzy import fuzz

## The only public function you need
# Input an artist name, e.g. "Black Sabbath"
# Output an array of tuples characterizing songs
# Tuple format:
#   (artist, track, code, version)
def getKaraokeSongs(artist):
    artist_processed = processArtist(artist)
    query = f"https://search.healsonic.com/assets/php/search.php?kw={artist_processed}&lang=English"
    res = requests.get(query)
    if (res.status_code != 200):
        raise ConnectionError("Query to HealSonic Karaoke was not completed successfully")
    songList = res.json()
    return [(song['a'], song['t'], song['r'], song['v']) for song in songList if similarTo(song['a'], artist)]



## Helper functions

# Process a string so it fits into a url
# e.g. "Black Sabbath" -> "Black%27Sabbath"
def processArtist(artist):
    return urllib.parse.quote(artist)

# Returns a boolean whether str1 is similar enough to str2 (for artist matching)
# String-lengths must differ by no more than 1, and must pass fuzzy matching > 0.6.
def similarTo(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    return fuzz.ratio(str1, str2) > 60 and abs(len(str1)-len(str2)) <= 1
