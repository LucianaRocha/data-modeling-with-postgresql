import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, orient='records', lines=True)

    # insert song record
    columns_song = ['song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = df[columns_song]
    song_data = song_data.values
    song_data = song_data.tolist()

    cur.execute(song_table_insert, song_data[0])
       
    # insert artist record
    columns_artists = ['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']
    artist_data = df[columns_artists]
    artist_data = artist_data.values
    artist_data = artist_data.tolist()
    
    cur.execute(artist_table_insert, artist_data[0])
 
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, orient='records', lines=True)

    # filter by NextSong action
    df = df.query('page == "NextSong"')

    # convert timestamp column to datetime
    df = df.astype({'ts':'datetime64[ms]'})
    
    # insert time data records
    time_df = pd.DataFrame({'start_time': pd.Series(df.ts),
                        'hour': pd.Series(df.ts).dt.hour,
                        'day': pd.Series(df.ts).dt.day,
                        'week': pd.Series(df.ts).dt.week,
                        'month': pd.Series(df.ts).dt.month,
                        'year': pd.Series(df.ts).dt.year,
                        'weekday': pd.Series(df.ts).dt.weekday
                       })                    

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, row)

    # load user table
    columns_users = ['userId', 'firstName', 'lastName', 'gender', 'level']
    user_df = df[columns_users]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    # load songplay table
    columns_songplay = ['ts','userId', 'level','song','artist','sessionId','location','userAgent','length']
    df_songplay = df[columns_songplay]
    
    # insert songplay records
    for index, row in df_songplay.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

if __name__ == "__main__":
    main()