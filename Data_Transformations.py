import pandas as pd
import numpy as np

# read in our data 
artist = pd.read_csv('./data/artist.csv')
album = pd.read_csv('./data/album.csv')
track = pd.read_csv('./data/track.csv')
track_feat = pd.read_csv('./data/track_feat.csv')

# create function to check if there are duplicate row values in the dfs
def check_for_dups(df, table):
    '''Function takes in a pandas dataframe (df) and the name if the df as a string (table)'''
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