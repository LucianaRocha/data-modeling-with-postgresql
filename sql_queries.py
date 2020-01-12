# DROP TABLES if exist in sparkifydb database
songplay_table_drop = "DROP table IF EXISTS songplays;"
user_table_drop = "DROP table IF EXISTS users;"
time_table_drop = "DROP table IF EXISTS time;"
artist_table_drop = "DROP table IF EXISTS artists;"
song_table_drop = "DROP table IF EXISTS songs;"

# CREATE TABLES in sparkifydb database
songplay_table_create = (
    "CREATE table IF NOT EXISTS songplays (" \
        "songplay_id SERIAL," \
        "start_time TIMESTAMP," \
        "user_id int," \
        "level varchar," \
        "song_id varchar," \
        "artist_id varchar," \
        "session_id int," \
        "location varchar," \
        "user_agent varchar, " \
        "PRIMARY KEY (songplay_id)," \
        "FOREIGN KEY (start_time) REFERENCES time (start_time)," \
        "FOREIGN KEY (user_id) REFERENCES users (user_id)," \
        "FOREIGN KEY (song_id) REFERENCES songs (song_id)," \
        "FOREIGN KEY (artist_id) REFERENCES artists (artist_id))"
    )

song_table_create = (
    "CREATE table IF NOT EXISTS songs (" \
        "song_id varchar NOT NULL," \
        "title varchar," \
        "artist_id varchar NOT NULL," \
        "year int," \
        "duration numeric," \
        "PRIMARY KEY (song_id))"
    )

artist_table_create = (
    "CREATE table IF NOT EXISTS artists (" \
        "artist_id varchar NOT NULL," \
        "name varchar," \
        "location varchar," \
        "latitude numeric," \
        "longitude numeric," \
        "PRIMARY KEY (artist_id))"
    )

time_table_create = (
    "CREATE table IF NOT EXISTS time (" \
        "start_time TIMESTAMP," \
        "hour int," \
        "day int," \
        "week int," \
        "month int," \
        "year int," \
        "weekday int," \
        "PRIMARY KEY (start_time))"
    )

user_table_create = (
    "CREATE table IF NOT EXISTS users (" \
        "user_id int," \
        "first_name varchar," \
        "last_name varchar," \
        "gender varchar," \
        "level varchar," \
        "PRIMARY KEY (user_id))"
    )

# INSERT RECORDS into tables
song_table_insert = (
    "INSERT INTO songs(" \
        "song_id," \
        "title," \
        "artist_id," \
        "year," \
        "duration)" \
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
        "artist_id," \
        "name," \
        "location," \
        "latitude," \
        "longitude)" \
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
        "start_time," \
        "hour," \
        "day," \
        "week," \
        "month," \
        "year," \
        "weekday)" \
        "VALUES (%s, %s, %s, %s, %s, %s, %s)" \
        "ON CONFLICT (start_time)" \
        "DO UPDATE " \
            "SET hour  = EXCLUDED.hour," \
                "day = EXCLUDED.day," \
                "week  = EXCLUDED.week," \
                "month = EXCLUDED.month;"
)

user_table_insert = (
    "INSERT INTO users(" \
        "user_id," \
        "first_name," \
        "last_name," \
        "gender," \
        "level) " \
        "VALUES (%s, %s, %s, %s, %s)" \
        "ON CONFLICT (user_id)" \
        "DO UPDATE " \
            "SET first_name  = EXCLUDED.first_name," \
                "last_name  = EXCLUDED.last_name," \
                "gender  = EXCLUDED.gender," \
                "level  = EXCLUDED.level;"
)

songplay_table_insert = (
    "INSERT INTO songplays(" \
        "start_time," \
        "user_id," \
        "level," \
        "song_id," \
        "artist_id," \
        "session_id," \
        "location," \
        "user_agent) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
) 

# FIND songid and artistid to load into songplays
song_select = (
    "SELECT " \
        "songs.song_id as songid," \
        "songs.artist_id as artistid " \
    "FROM songs songs " \
    "INNER JOIN artists artists ON songs.artist_id = artists.artist_id " \
    "WHERE " \
        "songs.title = %s " \
        "AND artists.name = %s " \
        "AND songs.duration = %s " \
    "ORDER BY " \
        "songs.song_id asc"
)

# QUERY LISTS to create and drop tables
create_table_queries = [
    song_table_create,
    artist_table_create,
    time_table_create,
    user_table_create,
    songplay_table_create
    ]
drop_table_queries = [
    song_table_drop,
    artist_table_drop,
    time_table_drop,
    user_table_drop,
    songplay_table_drop
    ]