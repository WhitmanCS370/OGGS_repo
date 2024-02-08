import sys
import os

class FileManager():
    def __init__(self):
        self.os = os

    def rename(self,dir, oldFile, newFile):

        """
        This method will take in a target directory, target file, and a new file name for the
        target file the target file will be renamed to the new file name and kept in the same
        directory.

        TODO: 
         - handle file path, make rename only take in a filename and a new filename, and a directory
         - implement tests for this 

        """
        try:
            self.os.rename(oldFile, newFile)
        except FileNotFoundError:
            print("file: " + str(oldFile) + "not found")
        except FileExistsError: 
            print("file: " + str(newFile) + " already exists")


    def delete(self, fileName):
        """
        This method will delete a specific file from a directory given the path to that file.


        TODO: 
         - tests
         - should we take directory as an arguemnt or the relative path to that file?
         - 
        """
        try:
            self.os.remove(fileName)
        except FileNotFoundError:
            print("file" + str(fileName) + "not found")

    def add_file(self, filePath, dest):
        pass

    def list_files(self, dest):
        pass


# manager = FileManager() # testing

# manager.rename("./sounds/coffee-slurp-2.wav", "coffee-slurp2.wav") # testing