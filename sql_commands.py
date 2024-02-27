import os
import sqlite3
from audio import *

class databaseManager():
    """
    This class will manage the database for the audio library. It will be responsible for
    creating the database, adding, deleting, and updating records in the database, and
    querying the database.
    """
    soundFilePath = "./sounds/"
    def __init__(self):
        self.conn = sqlite3.connect('audio_library.db')
        self.cursor = self.conn.cursor()
        self.os = os
        self.directories = self.os.listdir("./sounds/")
        
    def add_audio_file(self, title, artist, album, genre, filepath, duration):
        """
        This method will move a new audio file to the sound library and update database with the new file.
        """
        insertPath = self.soundFilePath + title + ".mp3"
        self.os.rename(filepath, insertPath)

        self.cursor.execute("""
            INSERT INTO audio_files (title, artist, album, genre, filepath, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, artist, album, genre, insertPath, duration))
        self.conn.commit()