import sqlite3
def init():
    """
    This function will initialize the database with the necessary tables.
    
    WILL WIPE ALL DATA IN THE DATABASE
    """
    # Connect to the database
    conn = sqlite3.connect('audio_library.sqlite')
    cursor = conn.cursor()
    
    # Drop ALL tables, revert to clean slate
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = cursor.fetchall()
    # for table in tables:
    #     cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")

    # Create the tables
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
    CREATE TABLE IF NOT EXISTS file_tags (
        id INTEGER PRIMARY KEY,
        tag_id INTEGER,
        audio_file_id INTEGER,
        FOREIGN KEY (tag_id) REFERENCES tags(id),
        FOREIGN KEY (audio_file_id) REFERENCES audio_files(id)
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    try:
        confirmation = ""
        while confirmation.lower() not in ["y", "n"]:
            confirmation = input("This will completely reset the database, are you sure? Y/N: ")
            if confirmation.lower() == "y":
                print("Initializing database...")
                init()
                print("Database initialized, exiting script.")
                break
            elif confirmation.lower() == "n":
                print("Cancelling database reset, exiting script.")
                break
            else:
                print("Invalid input, please enter Y or N.")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise