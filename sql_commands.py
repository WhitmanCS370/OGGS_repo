import os
import sqlite3
import wave
from audio import *
from database_init import init


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
        
    # def add_audio_file(self, title, artist, album, genre, filepath, duration):
    #     """
    #     This method will move a new audio file to the sound library and update database with the new file.
    #     """
    #     insertPath = self.soundFilePath + title + ".mp3"
    #     self.os.rename(filepath, insertPath)

    #     self.cursor.execute("""
    #         INSERT INTO audio_files (title, artist, album, genre, filepath, duration)
    #         VALUES (?, ?, ?, ?, ?, ?)
    #     """, (title, artist, album, genre, insertPath, duration))
    #     self.conn.commit()

    def get_playlist_id(self, playlist):
        self.cursor.execute(
            """
                SELECT DISTINCT id FROM playlists
                WHERE name == (?);
            """,(playlist,)
        )
        playlistid = self.cursor.fetchall()
        return playlistid[0][0]

    def get_song_id(self, filename):
        self.cursor.execute(
            """
                SELECT DISTINCT id FROM audio_files
                WHERE title == (?);
            """,(filename,)
        )
        songid = self.cursor.fetchall()
        return songid[0][0]
    
    def get_tag_id(self, tag):
        self.cursor.execute(
            """
                SELECT DISTINCT id FROM tags
                WHERE name == (?);
            """,(tag,)
        )
        tagid = self.cursor.fetchall()
        return tagid[0][0]

    def get_filepath(self, filename):
        self.cursor.execute(
            """
                SELECT DISTINCT title, filepath FROM audio_files
                WHERE title == (?);
            """,(filename,)
        )
        path = self.cursor.fetchall()
        return path
    
    def get_duration(self, filepath): 
        with wave.open(filepath, 'rb') as wf:
            duration = float(wf.getnframes()) / wf.getframerate()
        return duration

    def add_from_file(self, title, filepath, artist = "NULL", album = "NULL", genre = "NULL"):
        """
        album, artist, genre allowed null
        calculate duration from filepath
        """
        duration = self.get_duration(filepath)
        self.cursor.execute("""
            INSERT INTO audio_files (title, artist, album, genre, filepath, duration)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (title, artist, album, genre, filepath, duration))
        self.conn.commit()

    def add_playlist(self, name):
        """
        This method will add a new playlist to the database.
        """
        self.cursor.execute("""
            INSERT INTO playlists (name)
            VALUES (?)
        """, (name,))
        self.conn.commit()

    def song_to_playlist(self, playlist ,song):
        """
        add a song to a playlist.
        """
        playlistid = self.get_playlist_id(playlist)
        songid = self.get_song_id(song)
        self.cursor.execute("""
            INSERT INTO playlist_items (playlist_id, audio_file_id)
            VALUES (?, ?)
        """, (playlistid, songid))
        self.conn.commit()



    def get_playlist(self, playlist):
        """
        get all songs in a playlist
        """
        playlistid = self.get_playlist_id(playlist)
        self.cursor.execute("""
            SELECT DISTINCT audio_files.*
            FROM audio_files
            JOIN playlist_items ON audio_files.id = playlist_items.audio_file_id
            WHERE playlist_items.playlist_id = (?);
        """, (playlistid,))
        files = self.cursor.fetchall()
        return files

    def clear_tables(self):
        """
        helper function to clear tables for testing or reseting the database
        """

        self.cursor.execute("""
            DELETE FROM audio_files;
        """)
        self.cursor.execute("""
            DELETE FROM playlists;
        """)
        self.cursor.execute("""
            DELETE FROM playlist_items;
        """)
        self.conn.commit()


    def add_tag(self, name, desc):
        """
        add a tag to the database
        """
        self.cursor.execute("""
            INSERT INTO tags (name, desc)
            VALUES (?, ?)
        """, (name, desc))
        self.conn.commit()


    def add_tag_to_file(self, tag, filename):
        """
        add a tag to a file
        """
        tagid = self.get_tag_id(tag)
        songid = self.get_song_id(filename)
        self.cursor.execute("""
            INSERT INTO file_tag (tag_id, audio_file_id)
            VALUES (?, ?)
        """, (tagid, songid))
        self.conn.commit()


if __name__ == "__main__":
    init()
    dbm = databaseManager()
    
    dbm.add_from_file("toast", "sounds/old-sounds/toaster.wav")
    dbm.add_from_file("toast-2", "sounds/old-sounds/toaster-2.wav")
    dbm.add_playlist("test_playlist")
    dbm.song_to_playlist("test_playlist", "toast")
    dbm.song_to_playlist("test_playlist", "toast-2")
    print(dbm.get_playlist("test_playlist"))
    dbm.clear_tables()
