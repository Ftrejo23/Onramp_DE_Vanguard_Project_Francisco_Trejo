import pandas as pd
import sqlite3

print('Connecting to database...')
# connect to database
db_conn = sqlite3.connect('data/sql_db/spotify_data.db')
print('Connection successful.')

# create a function to run queries and output pandas dataframe
def Q(query, db=db_conn):
    print(pd.read_sql(query, db))

'Outputs of queries/views shown in jupyter notebook, see readme for more info'

print('Creating necessary views...\n')
# This will drop the view if it exists. Need this in order to rerun code.
db_conn.execute('''DROP VIEW IF EXISTS top_5_songs_ms_view ;''')

db_conn.execute('''
CREATE VIEW top_5_songs_ms_view AS
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
-- only want songs ranked in the top 5
WHERE song_duration_rank_by_artist BETWEEN 1 AND 5
ORDER BY artist_name ASC, song_duration_rank_by_artist ASC;
''')

db_conn.execute('''DROP VIEW IF EXISTS top_10_artist_num_followers_view;''')

db_conn.execute('''
CREATE VIEW top_10_artist_num_followers_view AS
SELECT artist_name, genre, followers, popularity
FROM Artist
ORDER BY followers DESC
LIMIT 10;
''')

db_conn.execute('''DROP VIEW IF EXISTS top_5_songs_tempo_view;''')

db_conn.execute('''
CREATE VIEW top_5_songs_tempo_view AS
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
WHERE tempo_rank_by_artist BETWEEN 1 AND 5
ORDER BY artist_name ASC, tempo_rank_by_artist ASC;
''')

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

Q('''
SELECT name 
FROM sqlite_schema 
WHERE type = 'view';
''')

print('\nAll views created successfully!')

# commit changes to the database
db_conn.commit()

# close database connection
db_conn.close()