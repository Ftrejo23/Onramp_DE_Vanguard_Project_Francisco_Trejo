import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

"""
    Make sure you have the following environment variables set:
        SPOTIPY_CLIENT_ID
        SPOTIPY_CLIENT_SECRET
        SPOTIPY_REDIRECT_URI
"""

print('Connecting to Spotipy...')
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
print('Success!!!\nGetting info for artists...')

# names of my favorite 20 artists!
names = ['Drake', 'J. Cole', 'JID', 'The Weeknd', 'Travis Scott', 
         'Baby Keem', 'Playboi Carti', 'Gunna', 'Don Toliver', 'Cordae', 
         'Lil Baby', 'Brent Faiyaz', 'Kanye', 'Lil Uzi Vert', 'Bryson Tiller',
         'Juice WRLD', 'Michael Jackson', 'Post Malone', 'Future', 'Nav']

# create main list to store artist info
artist_list = []
# create main list to store album info
album_list = []
# create main list to store track info
track_list = []
# create main list to store track feature info
track_feat_list = []

# iterate through list of artists and get needed info
for i, name in enumerate(names):
    
    # print status updates as data is pulled
    if i+1 == int(len(names)*.10):
        print('Status: 10%...')
    elif i+1 == int(len(names)*.50):
        print('Status: 50%...')
    elif i+1 == int(len(names)*.90):
        print('Status: 90%...')
        
    # create instance with artist search results
    results = spotify.search(q='artist:' + name, type='artist', market='US')

    # create dict for current artist values
    current_artist = {}

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
        current_artist['artist_uri'] = artist['uri']

        # add dict to list
        artist_list.append(current_artist)

        artist_uri = artist["uri"]


    # create instance with album search results for artist
    results_alb = spotify.artist_albums(artist_id = artist_uri, album_type = 'album', country = 'US', limit=12)
    
    # iterate through albums
    for alb in range(len(results_alb['items'])):
        # create dict for current album values
        current_album = {}

        album = results_alb['items'][alb]

        # check to see if album is the same as the previous album, if so skip to next iteration
        #(Spotify API has explicit and clean version as separate albums with same names)
        if album['name'] == results_alb['items'][alb-1]['name']:
            continue

        # add album id to dict
        current_album['album_id'] = album['id']

        # add album name to dict
        current_album['album_name'] = album['name']

        # add external url to dict
        current_album['external_url'] = album['external_urls']['spotify']

        # add image url to dict
        current_album['image_url'] = album['images'][0]['url']

        # add release date to dict
        current_album['release_date'] = album['release_date']

        # add total number of track to dict
        current_album['total_tracks'] = album['total_tracks']

        # add type to dict
        current_album['type'] = album['type']

        # add album uri to dict
        current_album['album_uri'] = album['uri']

        # add artist id to dict
        current_album['artist_id'] = artist['id']

        # add dict to list
        album_list.append(current_album)

        album_id = album['id']


        # create instance with track search results for album
        results_track = spotify.album_tracks(album_id = album_id, limit=50, offset=0)

        # iterate over each song in the album
        for song in range(len(results_track['items'])):

            # create dict for current track values
            current_track = {}
            track = results_track['items'][song]

            # add track id to dict
            current_track['track_id'] = track['id']

            # add song name to dict
            current_track['song_name'] = track['name']

            # add external url to dict
            current_track['external_url'] = track['external_urls']['spotify']

            # add song duration in ms to dict
            current_track['duration_ms'] = track['duration_ms']

            # add boolean value for whether or not song is explicit to dict
            current_track['explicit'] = track['explicit']

            # add disc number to dict
            current_track['disc_number'] = track['disc_number']

            # add type to dict
            current_track['type'] = track['type']

            # add song uri to dict
            current_track['song_uri'] = track['uri']

            # add album id to dict
            current_track['album_id'] = album['id']

            # add dict to list
            track_list.append(current_track)

            track_id = results_track['items'][song]['id']

            # create instance with track feature results for track
            results_track_feat = spotify.audio_features([track_id])

            # create dict for current track feature values
            current_track_feat = {}
            track_feat = results_track_feat[0]

            # add track id to dict
            current_track_feat['track_id'] = track_feat['id']

            # add danceability value to dict
            current_track_feat['danceability'] = track_feat['danceability']

            # add energy value to dict
            current_track_feat['energy'] = track_feat['energy']

            # add instrumentalness value to dict
            current_track_feat['instrumentalness'] = track_feat['instrumentalness']

            # add liveness value to dict
            current_track_feat['liveness'] = track_feat['liveness']

            # add loudness value to dict
            current_track_feat['loudness'] = track_feat['loudness']

            # add speechiness value to dict
            current_track_feat['speechiness'] = track_feat['speechiness']

            # add tempo value to dict
            current_track_feat['tempo'] = track_feat['tempo']

            # add type to dict
            current_track_feat['type'] = track_feat['type']

            # add valence value to dict
            current_track_feat['valence'] = track_feat['valence']

            # add song uri to dict
            current_track_feat['song_uri'] = track_feat['uri']

            # add dict to list
            track_feat_list.append(current_track_feat)
print('Data for artists successfully pulled!')
print('Saving data to .csv files...')

tables = [artist_list, album_list, track_list, track_feat_list]
table_names = ['artist_list', 'album_list', 'track_list', 'track_feat_list']

for table, table_name in zip(tables, table_names):
    df = pd.DataFrame(table)
    df.to_csv(f'./data/{table_name[:-5]}.csv', index=False)
    
print('Data saved successfully, ready for data transformations!')