# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplay;"
user_table_drop = "DROP table IF EXISTS users;"
song_table_drop = "DROP table IF EXISTS songs;"
artist_table_drop = "DROP table IF EXISTS artists;"
time_table_drop = "DROP table IF EXISTS time;"

# CREATE STAGING AREA: is a set of tables that represent a true copy of the data source
# SONGDATA and LOGFILES

songdata_table_create = (
    "CREATE table IF NOT EXISTS songdata (" \
        "artist_id varchar, artist_location varchar," \
        "artist_name varchar, song_id varchar, title varchar," \
        "year varchar)"
    )
  

logfiles_table_create = (
    "CREATE table IF NOT EXISTS logfiles (" \
        "artist varchar, auth varchar, firstName varchar," \
        "gender varchar, itemInSession int, lastName varchar," \
        "length varchar, level varchar, location varchar," \
        "method varchar, page varchar, registration varchar," \
        "sessionId varchar, song varchar, status varchar," \
        "ts varchar, userAgent text, userId varchar)"
    )

# CREATE TABLES 
 
songplay_table_create = (
    "CREATE table IF NOT EXISTS songplays (" \
        "songplay_id int, start_time TIMESTAMP, user_id int," \
        "level varchar, song_id varchar, artist_id varchar," \
        "session_id int, location varchar, user_agent varchar)"
    )

user_table_create = (
    "CREATE table IF NOT EXISTS users (" \
        "user_id int, first_name varchar, last_name varchar," \
        "gender varchar, level varchar, "
        "PRIMARY KEY (user_id))"
    )

song_table_create = (
    "CREATE table IF NOT EXISTS songs (" \
        "song_id varchar NOT NULL, title varchar," \
        "artist_id varchar NOT NULL," \
        "year int, duration numeric," \
        "PRIMARY KEY (song_id))"
    )

artist_table_create = (
    "CREATE table IF NOT EXISTS artists (" \
        "artist_id varchar NOT NULL," \
        "name varchar, location varchar," \
        "latitude numeric, longitude numeric, " \
        "PRIMARY KEY (artist_id))"
    )

time_table_create = (
    "CREATE table IF NOT EXISTS time (" \
        "start_time TIMESTAMP, hour numeric, day numeric," \
        "week numeric, month numeric, year numeric, weekday numeric," \
        "PRIMARY KEY (start_time))"
    )

# INSERT RECORDS

logfiles_table_insert = (
    "INSERT INTO logfiles(" \
        "artist, auth, firstName, gender, itemInSession, lastName," \
        "length, level, location, method, page, registration," \
        "sessionId, song, status, ts, userAgent, userId)" \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
)

songdata_table_insert = (
    "INSERT INTO songdata(" \
        "artist_id, artist_location, artist_name," \
        "song_id, title, year)" \
        "VALUES (%s, %s, %s, %s, %s, %s);"
) 

songplay_table_insert = (
    "INSERT INTO songplays(" \
        "songplay_id, start_time, user_id, level," \
        "song_id, artist_id, session_id, location, user_agent)" \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
) 

user_table_insert = (
    "INSERT INTO users(" \
        "user_id, first_name, last_name," \
        "gender, level)" \
        "VALUES (%s, %s, %s, %s, %s)" \
        "ON CONFLICT (user_id)" \
        "DO UPDATE " \
            "SET first_name  = EXCLUDED.first_name," \
                "last_name  = EXCLUDED.last_name," \
                "gender  = EXCLUDED.gender," \
                "level  = EXCLUDED.level;"
)

song_table_insert = (
    "INSERT INTO songs(" \
        "song_id, title, artist_id, year, duration)" \
        "VALUES (%s, %s, %s, %s, %s)" \
        "ON CONFLICT (song_id)" \
        "DO UPDATE " \
            "SET title  = EXCLUDED.title," \
                "artist_id  = EXCLUDED.artist_id," \
                "year  = EXCLUDED.year," \
                "duration  = EXCLUDED.duration;"
)

artist_table_insert = (
        "INSERT INTO artists(" \
        "artist_id, name, location, latitude, longitude)" \
        "VALUES (%s, %s, %s, %s, %s)" \
        "ON CONFLICT (artist_id)" \
        "DO UPDATE " \
            "SET name  = EXCLUDED.name," \
                "location = EXCLUDED.location," \
                "latitude  = EXCLUDED.latitude," \
                "longitude = EXCLUDED.longitude;"
)


time_table_insert = (
        "INSERT INTO time(" \
        "start_time, hour, day, week, month," \
        "year, weekday)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s)" \
        "ON CONFLICT (start_time)" \
        "DO UPDATE " \
            "SET hour  = EXCLUDED.hour," \
                "day = EXCLUDED.day," \
                "week  = EXCLUDED.week," \
                "month = EXCLUDED.month;"
)

# FIND SONGS

song_select = (
    "SELECT songs.song_id as songid, songs.artist_id as artistid " \
    "FROM songs songs INNER JOIN " \
    "artists artists ON songs.artist_id = artists.artist_id " \
    "WHERE songs.title = %s AND " \
        "artists.name = %s AND " \
        "songs.duration = %s " \
    "ORDER BY songs.song_id asc"
)

# QUERY LISTS
create_table_queries = [songdata_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create, logfiles_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]