import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import pandas as pd

"""
    Make sure you have the following environment variables set:
        SPOTIPY_CLIENT_ID
        SPOTIPY_CLIENT_SECRET
        SPOTIPY_REDIRECT_URI
"""

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
name = "Drake"

# create main list to store artist info
artist_list = []

# create dict for current artist values
current_artist = {}

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
artist_uri = ""
if len(items) > 0:
    artist = items[0]
    
    # add artist id to dict
    current_artist['artist_id'] = artist['id']
    
    # add artist name to dict
    current_artist['artist_name'] = artist['name']
    
    # add external url to dict
    current_artist['external_url'] = artist['external_urls']['spotify']
    
    # add 1st genre to dict
    current_artist['genre'] = artist['genres'][0]
    
    # add image url to dict
    current_artist['image_url'] = artist['images'][0]['url']
    
    # add followers to dict
    current_artist['followers'] = artist['followers']['total']
    
    # add popularity to dict
    current_artist['popularity'] = artist['popularity']
    
    # add type to dict
    current_artist['type'] = artist['type']
    
    # add artist uri to dict
    current_artist['type'] = artist['uri']
    
    artist_list.append(current_artist)
    
    # delete later!!!!!!
    pprint.pprint(artist)
    artist_uri = artist["uri"]
    print('\n', artist['name'], artist['images'][0]['url'], '\n')

    print(artist_list)

# results = spotify.artist_albums(artist_id = artist_uri, album_type = 'album', country = 'US')
# print('\n')
# pprint.pprint(results['items'][0])
# album_id = results['items'][0]['id']

# results = spotify.album_tracks(album_id = album_id, limit=50, offset=0)
# print('\n')
# pprint.pprint(results['items'][0])
# track_id = results['items'][0]['id']

# results = spotify.audio_features([track_id])
# print('\n')
# pprint.pprint(results)