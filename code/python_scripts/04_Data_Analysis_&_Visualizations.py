import pandas as pd
import sqlite3

print('Connecting to database...')
# connect to database
db_conn = sqlite3.connect('data/sql_db/spotify_data.db')
print('Connection successful.')

# create a function to run queries and output pandas dataframe
def Q(query, db=db_conn):
    return pd.read_sql(query, db)

'Outputs of queries/views shown in jupyter notebook, see readme for more info'

print('Creating necessary views...')
# This will drop the view if it exists. Need this in order to rerun code.
db_conn.execute('''DROP VIEW IF EXISTS top_songs_ms_view ;''')

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
SELECT *
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





# commit changes to the database
db_conn.commit()

# close database connection
db_conn.close()