import sqlite3
def init():
    # Connect to the database
    conn = sqlite3.connect('audio_library.db')
    cursor = conn.cursor()

    # Create the tables (if they don't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_files (
            id INTEGER PRIMARY KEY,
            title TEXT UNIQUE,
            artist TEXT,
            album TEXT, 
            genre TEXT,
            filepath TEXT,
            duration INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_items (
            id INTEGER PRIMARY KEY,
            playlist_id INTEGER,
            audio_file_id INTEGER,
            FOREIGN KEY (playlist_id) REFERENCES playlists(id),
            FOREIGN KEY (audio_file_id) REFERENCES audio_files(id) 
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        desc TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_tag (
        id INTEGER PRIMARY KEY,
        tag_id INTEGER,
        audio_file_id INTEGER,
        FOREIGN KEY (tag_id) REFERENCES tags(id),
        FOREIGN KEY (audio_file_id) REFERENCES audio_files(id)
    )
    """)
    conn.commit()
    conn.close()

