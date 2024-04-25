import os
from audio import *
import shutil 

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
        except (FileNotFoundError , FileExistsError):
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
    
    def duplicate_file(self,file, sql):
        srcFile=file
        if file[-5].isnumeric():
            num=int(file[-5])+1
            file=str(num).join(file.rsplit(str(num-1), 1))
        else: 
            hashlist = list(file)
            hashlist.insert(-4, '_2')
            file=''.join(hashlist)
        shutil.copyfile(".\\sounds\\"+srcFile,".\\sounds\\"+file) 
        sql.add_from_file(self, file, ".\\sounds\\")
        
if __name__ == '__main__':
    FileManager().list_files()