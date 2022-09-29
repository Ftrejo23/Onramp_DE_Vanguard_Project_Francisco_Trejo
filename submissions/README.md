# Onramp Data Engineer Vanguard Project - Francisco Trejo

## Contents

1. [Project Objective](#Project-Objective)
2. [Project Directory](#Project-Directory)
3. [Project Requirements](#Project-Requirements)
4. [Data Dictionary](#Data-Dictionary)
5. [Executive Summary](#Executive-Summary)
6. [Spotify Data Ingestion](#Spotify-Data-Ingestion)
7. [Data Transformations](#Data=Transformations)
8. [Data Storage](#Data-Storage)
9. [Data Analysis & Visualizations](#Data-Analysis-&-Visualizations)
10. [Conclusions & Recommendations](#Conclusions--Recommendations)
11. [Notes](#Notes)

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
### Quick links:
- [assets](./assets)
- [python_scripts](./code/python_scripts)
- [jupyter_notebooks](./code/jupyter_notebooks)
- [data](./data)

## Project Requirements
The following libraries were used in the project.
- Spotipy
- Pandas
- Numpy
- Sqlite3
- Seaborn
- Matplotlib

## Data Dictionary

Data dictionary taken from project repo found [here](https://github.com/onramp-io/vanguard_de_project).
#### Artist

|    column    |   datatype   |                              example                             |
|:------------:|:------------:|:----------------------------------------------------------------:|
|   artist_id  |  varchar(50) |                      7jy3rLJdDQY21OgRLCZ9sD                      |
|  artist_name | varchar(255) |                           Foo Fighters                           |
| external_url | varchar(100) |      https://open.spotify.com/artist/7jy3rLJdDQY21OgRLCZ9sD      |
|     genre    | varchar(100) |                         alternative metal                        |
|   image_url  | varchar(100) | https://i.scdn.co/image/ab6761610000e5eb9a43b87b50cd3d03544bb3e5 |
|   followers  |      int     |                             10156976                             |
|  popularity  |      int     |                                77                                |
|     type     |  varchar(50) |                              artist                              |
|  artist_uri  | varchar(100) |               spotify:artist:7jy3rLJdDQY21OgRLCZ9sD              |

#### Album

|    column    |   datatype   |                              example                             |
|:------------:|:------------:|:----------------------------------------------------------------:|
|   album_id   |  varchar(50) |                      2FfewmvnA0wctMD64KjOxP                      |
|  album_name  | varchar(255) |                            Dream Widow                           |
| external_url | varchar(100) |       https://open.spotify.com/album/2FfewmvnA0wctMD64KjOxP      |
|   image_url  | varchar(100) | https://i.scdn.co/image/ab67616d0000b273a57abaeb967f055948170bd6 |
| release_date |     date     |                            2022-03-25                            |
| total_tracks |      int     |                                 8                                |
|     type     |  varchar(50) |                               album                              |
|   album_uri  | varchar(100) |               spotify:album:2FfewmvnA0wctMD64KjOxP               |
|   artist_id  |  varchar(50) |                      7jy3rLJdDQY21OgRLCZ9sD                      |

#### Track
|    column    |   datatype   |                        example                        |
|:------------:|:------------:|:-----------------------------------------------------:|
|   track_id   |  varchar(50) |                 5k8kaD41vSP6l0Jhe9HzmY                |
| song_name    | varchar(255) |                         Encino                        |
| external_url | varchar(100) | https://open.spotify.com/track/5k8kaD41vSP6l0Jhe9HzmY |
|  duration_ms |      int     |                         98293                         |
|   explicit   |    boolean   |                          TRUE                         |
|  disc_number |      int     |                           1                           |
|     type     |  varchar(50) |                         track                         |
|   song_uri   | varchar(100) |          spotify:track:5k8kaD41vSP6l0Jhe9HzmY         |
|   album_id   |  varchar(50) |                 2FfewmvnA0wctMD64KjOxP                |

#### Track_Feature
|      column      |   datatype   |                example               |
|:----------------:|:------------:|:------------------------------------:|
|     track_id     |  varchar(50) |        5k8kaD41vSP6l0Jhe9HzmY        |
|   danceability   |    double    |                 0.277                |
|      energy      |    double    |                 0.992                |
| instrumentalness |    double    |                 0.836                |
|     liveness     |    double    |                 0.272                |
|     loudness     |    double    |                -6.237                |
|    speechiness   |    double    |                0.0856                |
|       tempo      |    double    |                103.494               |
|       type       |  varchar(50) |            audio_features            |
|      valence     |    double    |                 0.148                |
|     song_uri     | varchar(100) | spotify:track:5k8kaD41vSP6l0Jhe9HzmY |

For further explanation of Track_Feature values see [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features).

## Executive Summary
For this project, I pulled artist, album, song, and song features using the Spotify API. Over 2000 rows of data were successfully pulled and then saved as 4 csv files. The data was then checked for duplicate values subsequently removing any that were present in the data. Once the data was deduplicated then the data was checked for any null values. None were present in the data so I was able to move on to addressing the data types. There was a date that had to be changed to a datetime datatype. Once data was fully transformed final csv version were then saved.

The next step was to store our data locally using SQLite, the final csv files were loaded in and then using pandas functions the data frames were loaded into the database as tables. Once the data was loaded it was time to do some data analytics and visualizations. 6 different views were created, 3 addressed the prompts given and the rest were my own based on findings I was interested in sharing. Finally, 4 different visualizations were made to help increase insight and understanding of the data.

## [Spotify Data Ingestion](./code/python_scripts/01_Spotify_Data_Ingestion.py)
For this file, I loaded in the necessary imports and set up my environment variables for the Spotify API, Spotipy. From there a connection was established and my top 20 artists were chosen in a list of names. For each necessary table, I created lists to store dictionaries for each current artist, album, track, and track feature. Then I started pulling in the data for each of my 20 artists, iterating through the list of names and for each artist pulling in a max of 12 albums and all respective tracks and track features. Appending to our lists as each iteration ends. Then at the end, I saved lists as pandas data frames and then to csv files in the appropriate folder.

## [Data Transformations](./code/python_scripts/02_Data_Transformations.py)
In the data transformations file, I read in the raw data and then created a function that checks for potential duplicate values and prints out the table and what columns the potential duplicates are in for further exploration. Please see Jupiter notebooks for further analysis. Any duplicates were dropped from the corresponding data frame and since all tables are connected if albums were dropped then the associated tracks need to be dropped as well. I then created a function to check for null values in our data, none were found so good to move on. Lastly, I checked the data types of the column values to make sure that they matched the data dictionary that was given. I changed a date column to be a datetime data type and then saved final data frames as final csv files.

## [Data Storage](./code/python_scripts/03_Data_Storage.py)
Here I loaded in the final csv files and then connected them to my local database. Using pandas functions I was able to load the data frames into SQLite as tables with the correct data types. Finally, I committed the changes and closed the connection.

## [Data Analysis & Visualizations](./code/python_scripts/04_Data_Analysis_&_Visualizations.py)
For the final file, I connected to my local SQLite database and created 2 functions in the python file to query the database. Both functions take in a SQL query but one prints a pandas data frame and the other returns it. Then I created 6 different views, 3 required and 3 of my own, for these views I had to drop them if they existed and then create the view to make it easier to re-run the code. Then I printed a table of all views to ensure they were successfully created. I created 4 different visualizations using matplotlib and seaborn ensuring that each visualization had a title, x-label, y-label, and legend if applicable. To do this I had to query the database and return a pandas data frame for plotting. Any additional transformations were made to get the necessary data and then they were saved as PNG files in the appropriate folder. These visualizations were later combined into a PDF using a PDF editor. Finally, I committed all the changes and closed the database connection.

## Conclusions & Recommendations
I was able to successfully pull data using the Spotify API, transform the data, store it locally, and then analyze and create visualizations. Over 2000 rows of raw data was pulled and after data transformations and removing duplicates there were still over 1500 rows. The SQL database contains 4 tables along with 6 views. Using matplotlib and seaborn I was able to create 4 different visualizations of the data which was then saved into a PDF file. All deliverables were successfully met and I really am grateful for the opportunity and the challenge.

Given more time I would have loved to incorporate some sort of cloud storage either with GCP or AWS to better emulate a more real-life scenario in a business environment. Also pulling in more data from the API would be beneficial and provide more value for those on the Data Science / Data Analytics teams. Lastly, I would like to see how this sort of project would be done in a team environment using GitHub, different branches, and having to deal with merge commits all of which would provide a valuable learning experience.

## Notes
I chose to have both .ipynb and .py files because I believe for certain portions of the project it was better to show the outputs and further elaborate on my thought process using a jupyter notebook. The code on both is identical but in the jupyter notebooks I was able to make comments in markdown and see the outputs which aided in my thought process. I was able to further show how I came to do certain things such as the data transformations, views, and visualizations.