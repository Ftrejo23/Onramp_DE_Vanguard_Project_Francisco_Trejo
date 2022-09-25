import pandas as pd
import numpy as np

# read in our data 
artist = pd.read_csv('./data/artist.csv')
album = pd.read_csv('./data/album.csv')
track = pd.read_csv('./data/track.csv')
track_feat = pd.read_csv('./data/track_feat.csv')

# create function to check if there are duplicate row values in the dfs
def check_for_dups(df, table):
    '''Function takes in a pandas dataframe (df) and the name of the df as a string (table)'''
    potential_dups = []
    # iterate through the columns in the df
    for col in df.columns:
        # check to see if the column values are numbers, if not continue
        if df.dtypes[col] != np.int64 and df.dtypes[col] != np.float64:
            # if 'count' and 'unique' are different then potential duplicate values
            if df[col].describe()['count'] != df[col].describe()['unique']:
                potential_dups.append(col)
    print(f'The following columns in {table} have potential duplicates: {potential_dups}')

# check all dfs for potential duplicate values
check_for_dups(artist, 'artist')
check_for_dups(album, 'album')
check_for_dups(track, 'track')
check_for_dups(track_feat, 'track_feat')

print('Removing duplicate values from data...')

# further EDA was done in jupyter notebook, see readme for more info
# drop duplicate albums with the same name
album.drop_duplicates(subset=['album_name'], inplace=True)
# get list of album ids from our deduplicated dataframe
final_alb_ids = album['album_id'].tolist()

# get tracks that are only in the albums from our deduplicated album dataframe
track = track[track['album_id'].isin(final_alb_ids)]
# drop duplicate tracks with the same track_id
track.drop_duplicates(subset=['track_id'], inplace=True)
# get list of album ids from our deduplicated dataframe
final_track_ids = track['track_id'].tolist()

# get track_feat that are only in the tracks from our deduplicated track dataframe
track_feat = track_feat[track_feat['track_id'].isin(final_track_ids)]
# drop duplicate tracks with the same track_id
track_feat.drop_duplicates(subset=['track_id'], inplace=True)

print('Duplicate values successfully removed!')

# function to quickly check if there are null values in the dataframes
def check_for_nulls(dfs, tables):
    '''Function takes in a list of pandas dataframe (dfs) and the name of the df as a list (tables)'''
    for df, table in zip(dfs, tables):
        if df.isnull().sum().sum() == 0:
            print(f'No null values in {table} dataframe!')
        else:
            print(f'{tables} has {df.isnull().sum().sum()} null value(s), further investigate.')

print('Checking data for null values...')
check_for_nulls([artist, album, track, track_feat], ['artist', 'album', 'track', 'track_feat'])