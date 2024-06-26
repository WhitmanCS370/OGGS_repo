import os
import sqlite3
import wave
import numpy as np
from logic import *
from database_init import init

class databaseManager():
    """
    This class will manage the database for the audio library. It will be responsible for
    creating the database, adding, deleting, and updating records in the database, and
    querying the database.
    """
    soundFilePath = "./sounds/"
    def __init__(self):
        self.conn = sqlite3.connect('audio_library.sqlite', check_same_thread=False)
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
        
    # START SONG METHODS
    def get_song_id(self, filename):
        try:
            self.cursor.execute(
                """
                    SELECT DISTINCT id FROM audio_files
                    WHERE title == (?);
                """,(filename,)
            )
            songid = self.cursor.fetchall()
            return songid[0][0] if songid else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def get_duration(self, filepath): 
        try:
            with wave.open(filepath, 'rb') as wf:
                duration = float(wf.getnframes()) / wf.getframerate()
            return duration
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    # END SONG METHODS

    # START PLAYLIST METHODS

    def get_playlist_id(self, playlist):
        try:
            self.cursor.execute(
                """
                    SELECT DISTINCT id FROM playlists
                    WHERE name == (?);
                """,(playlist,)
            )
            playlistid = np.array(self.cursor.fetchall())
            return playlistid[0][0] if playlistid else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def list_playlists(self):
        try:
            self.cursor.execute("""
                SELECT DISTINCT name FROM playlists;
            """)
            playlists = np.array(self.cursor.fetchall())
            return playlists.ravel()
        except Exception as e:
            print(f"An error occurred listing playlists: {e}")
            return None

    def get_playlist(self, playlist):
        try:
            playlistid = self.get_playlist_id(playlist)
            self.cursor.execute("""
                SELECT DISTINCT audio_files.filepath
                FROM audio_files
                JOIN playlist_items ON audio_files.id = playlist_items.audio_file_id
                WHERE playlist_items.playlist_id = (?);
            """, (playlistid,))
            files = np.array(self.cursor.fetchall())
            return files.ravel()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def add_playlist(self, name):
        try:
            self.cursor.execute("""
                INSERT INTO playlists (name)
                VALUES (?)
            """, (name,))
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def song_to_playlist(self, playlist ,songs):
        try:
            playlistid = self.get_playlist_id(playlist)
            if type(songs)==str:
                print(songs)
                songs=[songs]
            for song in songs:
                title, ext = os.path.splitext(os.path.basename(song))
                # title = song.split("/")[-1].split(".")[0]
                songid = self.get_song_id(title)
                self.cursor.execute("""
                    INSERT INTO playlist_items (playlist_id, audio_file_id)
                    VALUES (?, ?)
                """, (playlistid, songid))
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def show_playlist(self, playlist):
        try:
            self.cursor.execute("""
                SELECT DISTINCT audio_files.title
                FROM audio_files
                JOIN playlist_items ON audio_files.id = playlist_items.audio_file_id
                WHERE playlist_items.playlist_id = (?); 
            """, (playlist,))
            songs = np.array(self.cursor.fetchall())
            return songs.ravel()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    # END PLAYLIST METHODS

    # START FILE METHODS
        
    def get_filepath(self, filename):
        try:
            self.cursor.execute(
                """
                    SELECT DISTINCT filepath FROM audio_files
                    WHERE title == (?);
                """,(filename,)
            )
            path = np.array(self.cursor.fetchall())
            return path[0][0] if path[0][0] else None
        except Exception as e:
            print("add")
            print(f"An error occurred: {e}")
            print("as")
            return None
    
    def get_name(self, filepath):
        try:
            self.cursor.execute(
                """
                    SELECT DISTINCT title FROM audio_files
                    WHERE filepath == (?);
                """,(filepath,)
            )
            path = np.array(self.cursor.fetchall())
            return path[0][0] if path[0][0] else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def add_from_file(self, filepath):
        try:
            duration = self.get_duration(filepath)
            root, ext = os.path.splitext(os.path.basename(filepath))
            self.cursor.execute("""
                INSERT INTO audio_files (title, filepath, duration)
                VALUES (?, ?, ?);
            """, (root, filepath, duration))
            self.conn.commit()
            self.add_tag_to_file(ext, root)
        except sqlite3.IntegrityError:
            print("File already exists in the database.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def delete_file_by_name(self,filename):
        try:
            self.cursor.execute(
                """
                DELETE FROM audio_files WHERE title==(?);
                """,(filename,)
            )
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None            

    def list_files(self):
        try:
            self.cursor.execute("""
                SELECT DISTINCT title FROM audio_files;
            """)
            files = np.array(self.cursor.fetchall())
            return files.ravel() if files.size > 0 else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def rename(self, oldFileName, newFileName, newFilepath):
        try:
            self.cursor.execute("""
                UPDATE audio_files
                SET title = ?
                WHERE title = ?;
            """, (newFileName, oldFileName))
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_all_from_file(self, filename):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM audio_files
                    WHERE title == (?);
                """,(filename,)
            )
            path=self.cursor.fetchall()
            self.conn.commit()

            return path[0] if path[0] else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_all_from_filepath(self, filepath):
        try:
            self.cursor.execute(
                """
                    SELECT * FROM audio_files
                    WHERE filepath == (?);
                """,(filepath,)
            )
            path=self.cursor.fetchall()
            self.conn.commit()
            return path[0] if path[0] else None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    # END FILE METHODS

    # START TAG METHODS
    
    def get_tag_id(self, tag):
        try:
            self.cursor.execute(
                """
                    SELECT DISTINCT id FROM tags
                    WHERE name == (?);
                """,(tag,)
            )
            tagid = self.cursor.fetchall()
            return tagid[0][0] if tagid else None
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_tags(self):
        try:
            self.cursor.execute("""
                SELECT DISTINCT name FROM tags;
            """)
            tags = np.array(self.cursor.fetchall())
            return tags.ravel() if tags.size > 0 else None
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_tag(self, name):
        try:
            self.cursor.execute("""
                INSERT INTO tags (name)
                VALUES (?)
            """, (name,))
            self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_tag_to_file(self, tag, songs):
        try:
            tagid = self.get_tag_id(tag)
            if type(songs)==str:
                songs=[songs]
            for song in songs:
                title, ext = os.path.splitext(os.path.basename(song))
                # title = song.split("/")[-1].split(".")[0]
                songid = self.get_song_id(title)
                self.cursor.execute("""
                    INSERT INTO file_tags (tag_id, audio_file_id)
                    VALUES (?, ?)
                """, (tagid, songid))
                self.conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


    def get_from_tag(self, tag):
        try:
            tagid = self.get_tag_id(tag)
            self.cursor.execute("""
                SELECT DISTINCT audio_files.title
                FROM audio_files
                JOIN file_tags ON audio_files.id = file_tags.audio_file_id
                WHERE file_tags.tag_id = (?);
            """, (tagid,))
            files = np.array(self.cursor.fetchall())
            return files.ravel()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def tags_from_file(self, file):
        try:
            fileID = self.get_song_id(file)
            self.cursor.execute("""
                SELECT DISTINCT tags.name
                FROM tags
                JOIN file_tags ON tags.id = file_tags.tag_id
                WHERE file_tags.audio_file_id = ?;
            """, (fileID,))
            tags = np.array(self.cursor.fetchall())
            return tags.ravel()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None    
        
        # END TAG METHODS
    

    # helper methods for testing
    def clear_tables(self):
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_all(self):
        try:
            for file in self.directories:
                if file.endswith(".wav"):
                    self.add_from_file( "./sounds/" + file)
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    init()
    dbm = databaseManager()
    dbm.add_all()
    print(dbm.list_files())
    # dbm.add_from_file("toast", "sounds/old-sounds/toaster.wav")
    # dbm.add_from_file("toast-2", "sounds/old-sounds/toaster-2.wav")
    # dbm.add_playlist("test_playlist")
    # dbm.song_to_playlist("test_playlist", "toast")
    # dbm.song_to_playlist("test_playlist", "toast-2")
    # print(dbm.get_playlist("test_playlist"))
    dbm.clear_tables()
