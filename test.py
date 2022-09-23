import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import pprint

"""
    Make sure you have the following environment variables set:
        SPOTIPY_CLIENT_ID
        SPOTIPY_CLIENT_SECRET
        SPOTIPY_REDIRECT_URI
"""

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
name = "Drake"

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
artist_uri = ""
if len(items) > 0:
    artist = items[0]
    pprint.pprint(artist)
    artist_uri = artist["uri"]
    print('\n', artist['name'], artist['images'][0]['url'], '\n')

results = spotify.artist_albums(artist_id = artist_uri, album_type = 'album', country = 'US')
print('\n')
pprint.pprint(results['items'][0])
album_id = results['items'][0]['id']

results = spotify.album_tracks(album_id = album_id, limit=50, offset=0)
print('\n')
pprint.pprint(results['items'][0])
track_id = results['items'][0]['id']

results = spotify.audio_features([track_id])
print('\n')
pprint.pprint(results)