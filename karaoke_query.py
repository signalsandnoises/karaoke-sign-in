import urllib.parse
import requests

## Defines functions to query the karaoke database

## The only public function you need
# Input an artist name, e.g. "Black Sabbath"
# Output an array of tuples characterizing songs
# Tuple format:
#   (artist, track, code, version)
def getKaraokeSongs(artist):
    artist = processArtist(artist)
    query = f"https://search.healsonic.com/assets/php/search.php?kw={artist}&lang=English"
    res = requests.get(query)
    if (res.status_code != 200):
        raise ConnectionError("Query to HealSonic Karaoke was not completed successfully")
    songList = res.json()
    return [(song['a'], song['t'], song['r'], song['v']) for song in songList]



## Helper functions

# Process a string so it fits into a url
# "Black Sabbath" -> "Black%27Sabbath"
def processArtist(artist):
    return urllib.parse.quote(artist)
