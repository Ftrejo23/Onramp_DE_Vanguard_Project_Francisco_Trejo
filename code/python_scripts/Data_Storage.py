import pandas as pd
import sqlite3

# read in transformed data
artist_df = pd.read_csv('../../data/final_artist.csv')
# need to make sure release_dates gets read in as a datetime
album_df = pd.read_csv('../../data/final_album.csv', parse_dates=['release_date'])
track_df = pd.read_csv('../../data/final_track.csv')
track_feat_df = pd.read_csv('../../data/final_track_feat.csv')

