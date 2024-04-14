import os
from audio import *

class FileManager():

    def __init__(self):
        self.os = os
        self.path = "./sounds/" # universal path to the sound archive

    def rename_file(self, oldFileName: str, newFileName: str):

        """
        Rename a file given the old file name and the new file name.
        """
        try:
            self.os.rename(self.path + oldFileName, self.path + newFileName)
        except FileNotFoundError:
            print(f"file: {oldFileName} not found")

    def delete_file(self, fileName: str):
        """
        Delete a specific file given filename.
        """
        try:
            self.os.remove(self.path + str(fileName))
        except FileNotFoundError:
            print(f"file: {fileName} not found")



    def add_file(self, fileOriginPath: str):
        """
        add a file to the sound archive
        Does not add to database, will require updating the database
        """
        try:
            self.os.rename(fileOriginPath, self.path + str(os.path.basename(fileOriginPath)))
        except FileNotFoundError:
            print(f"file: {fileOriginPath} not found")

    def add_file_menu(self):
        """
        TODO: 
         - add a menu for adding a file, like the one that show up in browsers for uploading files
        """
        raise NotImplementedError


    def list_files(self):
        """
        List all files in sounds folder
         """
        try:
            return self.os.listdir(self.path)
        except FileNotFoundError:
            print("No files found in archive")

if __name__ == '__main__':
    FileManager().list_files()