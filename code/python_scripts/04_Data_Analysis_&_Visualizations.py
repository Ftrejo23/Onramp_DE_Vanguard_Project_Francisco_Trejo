import pandas as pd
import sqlite3

print('Connecting to database...')
# connect to database
db_conn = sqlite3.connect('data/sql_db/spotify_data.db')
print('Connection successful.')

'Outputs of queries/views shown in jupyter notebook, see readme for more info'