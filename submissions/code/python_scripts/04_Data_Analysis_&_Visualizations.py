import pandas as pd
import numpy as np
import sqlite3
import seaborn as sns
import matplotlib.pyplot as plt 
from matplotlib.patches import Patch
plt.style.use('fivethirtyeight')

print('Connecting to database...')
# connect to database
db_conn = sqlite3.connect('submissions/data/sql_db/spotify_data.db')
print('Connection successful.\n')

# create a function to run queries and print pandas dataframe
def Q(query, db=db_conn):
    '''takes in SQL query and prints a pandas dataframe'''
    print(pd.read_sql(query, db))

# create a function to run queries and print pandas dataframe
def Q_df(query, db=db_conn):
    '''takes in SQL query and returns a pandas dataframe'''
    return(pd.read_sql(query, db))

'Outputs of queries/views shown in jupyter notebook, see readme for more info'

print('Creating necessary views...\n')

# Top 10 songs by artist in terms of duration_ms
# This will drop the view if it exists. Need this in order to rerun code.
db_conn.execute('''DROP VIEW IF EXISTS top_10_songs_ms_view;''')

db_conn.execute('''
CREATE VIEW top_10_songs_ms_view AS
WITH top_songs_by_artist_cte AS 
-- subquery for cte, want necessary columns and additional column that ranks songs by duration grouped by artist
(SELECT ar.artist_name, t.song_name, a.album_name, t.duration_ms,
    DENSE_RANK() OVER (PARTITION BY ar.artist_name ORDER BY t.duration_ms DESC) as song_duration_rank_by_artist
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
LEFT JOIN Track t 
    ON a.album_id = t.album_id
ORDER BY t.duration_ms DESC)
-- query the cte for top 5 longest songs by artist
SELECT *
FROM top_songs_by_artist_cte
-- only want songs ranked in the top 10
WHERE song_duration_rank_by_artist BETWEEN 1 AND 10
ORDER BY artist_name ASC, song_duration_rank_by_artist ASC;
''')

# Top 20 artists in the database by # of followers
db_conn.execute('''DROP VIEW IF EXISTS top_20_artist_num_followers_view;''')

db_conn.execute('''
CREATE VIEW top_20_artist_num_followers_view AS
SELECT artist_name, genre, followers, popularity
FROM Artist
ORDER BY followers DESC
LIMIT 20;
''')

# Top 10 songs by artist in terms of tempo
db_conn.execute('''DROP VIEW IF EXISTS top_10_songs_tempo_view;''')

db_conn.execute('''
CREATE VIEW top_10_songs_tempo_view AS
WITH top_tempo_cte AS
-- subquery for cte, need to rank songs by tempo
(SELECT ar.artist_name, t.song_name, tf.tempo,
    DENSE_RANK() OVER (PARTITION BY ar.artist_name ORDER BY tf.tempo DESC) as tempo_rank_by_artist
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
LEFT JOIN Track t 
    ON a.album_id = t.album_id
LEFT JOIN Track_Feature tf
    ON t.track_id = tf.track_id)
-- query the cte for top 5 tracks with highest tempo
SELECT *
FROM top_tempo_cte
WHERE tempo_rank_by_artist BETWEEN 1 AND 10
ORDER BY artist_name ASC, tempo_rank_by_artist ASC;
''')

# Top 10 Artists with most explicit tracks
db_conn.execute('''DROP VIEW IF EXISTS top_10_explicit_artist_view;''')

db_conn.execute('''
CREATE VIEW top_10_explicit_artist_view AS
SELECT ar.artist_name, SUM(t.explicit) as num_explicit_tracks
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
LEFT JOIN Track t 
    ON a.album_id = t.album_id
GROUP BY ar.artist_name
ORDER BY num_explicit_tracks DESC
LIMIT 10;
''')

# Top 5 genres with highest average energy
db_conn.execute('''DROP VIEW IF EXISTS top_5_genres_avg_energy_view;''')

db_conn.execute('''
CREATE VIEW top_5_genres_avg_energy_view AS
SELECT ar.genre, AVG(tf.energy) as avg_energy
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
LEFT JOIN Track t 
    ON a.album_id = t.album_id
LEFT JOIN Track_Feature tf
    ON t.track_id = tf.track_id
GROUP BY genre
ORDER BY avg_energy DESC
LIMIT 5;
''')

# Top 5 Artists with the most Deluxe/bonus albums
db_conn.execute('''DROP VIEW IF EXISTS top_5_artist_num_deluxe_view;''')

db_conn.execute('''
CREATE VIEW top_5_artist_num_deluxe_view AS
SELECT ar.artist_name, COUNT(a.album_name) as num_deluxe_albs
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
WHERE album_name LIKE '%deluxe%' OR album_name LIKE '%bonus%'
GROUP BY ar.artist_name
ORDER BY num_deluxe_albs DESC
LIMIT 5;
''')

# print out views in our database
Q('''
SELECT name 
FROM sqlite_schema 
WHERE type = 'view';
''')

print('\nAll views created successfully!\n')

'create visualizations, see jupyter notebook for plots and additional outputs, refer to readme'
print('Creating visualizations...')


# longest song duration per Artist
top_10_songs_df = Q_df('''
SELECT *
FROM top_10_songs_ms_view
''')

plt.figure(figsize=(15,10))

# want to get the longest songs for each artist
longest_songs = top_10_songs_df[top_10_songs_df['song_duration_rank_by_artist'] == 1]\
.sort_values(by='duration_ms', ascending=False)

# plot a bar chart of artist with longest songs
plt.bar(longest_songs['artist_name'], (longest_songs['duration_ms'] / 1000)/60, color='green', edgecolor='black')

# set title and labels
plt.title('Figure 1. Longest Song Duration per Artist', fontsize=20, fontweight='bold', loc='left')
plt.ylabel('Duration in minutes', fontsize=16, fontweight='bold')
plt.xlabel('Artist', fontsize=16, fontweight='bold')

# adjust x and y ticks
plt.xticks(rotation=75, fontsize=14)
y = np.arange(0, 14, 1)
plt.yticks(y)

plt.tight_layout()

# save figure as png file
plt.savefig('submissions/assets/longest_songs.png')


# correlation between energy and danceability of songs
track_feat_df = Q_df('''
SELECT *
FROM Track_Feature
''')

plt.figure(figsize=(15,10))

# get the correlation coefficient between 2 variables
corr_coeff = np.corrcoef(track_feat_df['energy'],track_feat_df['danceability'])[0][1]

# plot the scatter plot of energy vs danceability
plt.scatter(track_feat_df['energy'], track_feat_df['danceability'], 
            color='black', s=75, alpha=0.5, label='energy vs danceability')

# plot the correlation line
plt.plot(np.unique(track_feat_df.energy), 
         np.poly1d(np.polyfit(track_feat_df.energy, track_feat_df.danceability, 1))
         (np.unique(track_feat_df.energy)), 
         color='green', label=f'corr={round(corr_coeff, 2)}', alpha=0.8)

plt.legend(title='Legend', shadow=True)

# set title and labels
plt.title('Figure 2. Correlation Between Energy and Danceability of Songs', 
          fontsize=20, color='darkgreen', fontweight='bold', loc='left')
plt.ylabel('Danceability', fontsize=16, color='darkgreen', fontweight='bold')
plt.xlabel('Energy', fontsize=16, color='darkgreen', fontweight='bold')

# adjust x and y ticks
x = np.arange(0, 1.1, 0.1)
plt.xticks(x)
y = np.arange(0, 1.1, 0.1)
plt.yticks(y)

plt.tight_layout()

# save figure as png file
plt.savefig('submissions/assets/energy_vs_danceability.png');


# frequency of danceability
danceability = Q_df('''
SELECT *
FROM Track_Feature
''')

plt.figure(figsize=(15,10))
plt.hist(danceability['danceability'], color='black', edgecolor='white')

# set title and labels
plt.title('Figure 3. Danceability Frequency', 
          fontsize=20, color='darkgreen', fontweight='bold', loc='left')
plt.ylabel('Frequency', fontsize=16, color='darkgreen', fontweight='bold')
plt.xlabel('Danceability', fontsize=16, color='darkgreen', fontweight='bold')

# adjust x and y ticks
x = np.arange(0, 1.1, 0.1)
plt.xticks(x)
y = np.arange(0, 550, 50)
plt.yticks(y)

plt.tight_layout()

# save figure as png file
plt.savefig('submissions/assets/danceability_frequency.png');


# count of genre above/below median tempo
track_feat_df = Q_df('''
SELECT *
FROM Track_Feature
''')

# find median tempo
tempo_med = track_feat_df['tempo'].describe()['50%']

# query and create a column for wether a song is above/below median tempo
tempo_count_genre_df = Q_df(f'''
SELECT ar.genre, tf.tempo, 
    CASE WHEN tf.tempo >= {tempo_med} THEN 1
    ELSE 0 END AS song_above_below_med
FROM Artist ar
-- join necessary tables together
LEFT JOIN Album a 
    ON a.artist_id = ar.artist_id
LEFT JOIN Track t 
    ON a.album_id = t.album_id
LEFT JOIN Track_Feature tf
    ON t.track_id = tf.track_id
''')

plt.figure(figsize=(15,10))

# plot grouped bar chart
sns.countplot(x='genre', hue='song_above_below_med', data=tempo_count_genre_df, palette={1:'green', 0:'black'});

# set title and labels
plt.title('Figure 4. Genre vs Above/Below Median Tempo', fontsize=20, fontweight='bold', loc='left')

plt.ylabel('Count', fontsize=16, fontweight='bold')
plt.xlabel('Genre', fontsize=16, fontweight='bold')

# set color patches for legend
color_patches = [
    Patch(facecolor="green", label="above median tempo"),
    Patch(facecolor="black", label="below median tempo")
]

plt.legend(handles=color_patches, shadow=True, title='Legend')

# adjust xticks
plt.xticks(rotation=75, fontsize=14)

plt.tight_layout()

# save figure as png file
plt.savefig('submissions/assets/genre_above_below_med_tempo.png');

print('Visualizations created!\n')

# commit changes to the database
db_conn.commit()

print('Closing database connection...')
# close database connection
db_conn.close()
print('Database connection closed.')