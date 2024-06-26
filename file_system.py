import os
from os import path
from logic import *
import shutil 

class FileManager():

    def __init__(self):
        self.os = os
        self.path = os.path.join("sounds") # universal path to the sound archive

    def rename_file(self, oldFileName: str, newFileName: str):

        """
        Rename a file given the old file name and the new file name.
        """
        old_path = os.path.join(self.path, oldFileName)
        new_path = os.path.join(self.path, newFileName)
        try:
            os.rename(old_path, new_path)
        except FileNotFoundError:
            print(f"file: {oldFileName} not found")

    def delete_file(self, fileName: str):
        """
        Delete a specific file given filename.
        """
        if fileName[-4:]==".wav":
            file_path = os.path.join("sounds", fileName)
        else:
            file_path = os.path.join("sounds", fileName+".wav")
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"file: {fileName} not found")

    def add_file(self, fileOriginPath: str):
        """
        add a file to the sound archive
        Does not add to database, will require updating the database
        """
        try:
            assert self.os.path.isfile(fileOriginPath)
            assert fileOriginPath.endswith(".wav")
            newpath = self.os.path.join(self.path , str(os.path.basename(fileOriginPath)))
            self.os.rename(fileOriginPath, newpath)
            return newpath
        except FileNotFoundError:
            print(f"file: {fileOriginPath} not found")
        except AssertionError:
            print("File invalid")

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
    
    def duplicate_file(self,file, db):
        src_path = os.path.join(os.path.curdir,"sounds", file +".wav")
        if (("_" in file) and (file.split("_")[-1].isdigit())):
            num=int(file.split("_")[-1]) + 1
            file=file.split('_')[0] + "_" + str(num)
        else: 
            hashlist = list(file)
            hashlist.append('_2')
            file=''.join(hashlist)
        new_path = os.path.join(os.curdir, "sounds", file+".wav")
        shutil.copyfile(src_path, new_path)
        db.add_from_file(new_path)
        
if __name__ == '__main__':
    FileManager().list_files()