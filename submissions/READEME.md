# Onramp Data Engineer Vanguard Project - Francisco Trejo

## Contents

1. [Project Objective](#Problem-Statement)
2. [Project Directory](#Project-Directory)
3. [Project Requirements](#Project-Requirements)
4. [Data Dictionary](#Data-Dictionary)
5. [Executive Summary](#Executive-Summary)
6. [Data Collection](#Data-Collection)
7. [Data Cleaning](#Data-Cleaning)
8. [Exploratory Data Analysis](#Exploratory-Data-Analysis)
9. [Preprocessing](#Preprocessing)
10. [Modeling](#Modeling)
11. [Conclusions & Recommendations](#Conclusions--Recommendations)

## Project Objective

The objective of this project is to ingest, transform, store, and analyze Spotify data from my own personal top 20 artists. This will be done using the Spotify API, [Spotipy] (https://spotipy.readthedocs.io/en/master/#), to get info about the artist, their albums, and songs. The data will be stored in a SQLite database on our local machines where we will create views and visualizations for additional analytics.


## Project Directory
```
Onramp_DE_Vanguard_Project_Francisco_Trejo
|
|__ submissions
|   |__ assets
|   |   |__ danceability_frequency.png
|   |   |__ energy_vs_danceability.png
|   |   |__ genre_above_below_med_tempo.png
|   |   |__ longest_songs.png
|   |   |__ **visualization.pdf**
|   |__ code
|   |   |__ jupyter_notebooks
|   |   |   |__ 01_Spotify_Data_Ingestion.ipynb
|   |   |   |__ 02_Data_Transformations.ipynb
|   |   |   |__ 03_Data_Storage.ipynb
|   |   |   |__ 04_Data_Analysis_&_Visualizations.ipynb
|   |   |__ **python_scripts**
|   |   |   |__ 01_Spotify_Data_Ingestion.py
|   |   |   |__ 02_Data_Transformations.py
|   |   |   |__ 03_Data_Storage.py
|   |   |   |__ 04_Data_Analysis_&_Visualizations.py
|   |__ data
|   |   |__ sql_db
|   |   |   |__ **spotify_data.db**
|   |   |__ album.csv
|   |   |__ artist.csv
|   |   |__ final_album.csv
|   |   |__ final_artist.csv
|   |   |__ final_track.csv
|   |   |__ final_track_feat.csv
|   |   |__ track.csv
|   |   |__ track_feat.csv
|   |__ .gitignore
|   |__ README.md
|__ .gitignore
```