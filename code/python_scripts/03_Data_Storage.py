import pandas as pd
import sqlite3

print('Reading in transformed data...')
# read in transformed data
artist_df = pd.read_csv('data/final_artist.csv')
# need to make sure release_dates gets read in as a datetime
album_df = pd.read_csv('data/final_album.csv', parse_dates=['release_date'])
track_df = pd.read_csv('data/final_track.csv')
track_feat_df = pd.read_csv('data/final_track_feat.csv')
print('Data successfully loaded.')

print('Creating database connection...')
# create database connection
db_conn = sqlite3.connect('data/sql_db/spotify_data.db')

print('Loading in data into sql database...')
# load in data into sql database
artist_df.to_sql('Artist', con=db_conn, if_exists='replace', index=False)
album_df.to_sql('Album', con=db_conn, if_exists='replace', index=False)
track_df.to_sql('Track', con=db_conn, if_exists='replace', index=False)
track_feat_df.to_sql('Track_Feature', con=db_conn, if_exists='replace', index=False)
print('Success! Data loaded into sql!')

# commit changes to the database
db_conn.commit()

print('Closing database connection...')
# close database connection
db_conn.close()
print('Database connection closed.')


