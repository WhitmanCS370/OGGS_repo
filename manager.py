import os
from audio import *

class FileManager():

    def __init__(self):
        self.os = os
        self.directories = self.os.listdir("./sounds/")

    def rename(self, dir, oldFileName, newFileName):

        """
        This method will take in a target directory, target file, and a new file name for the
        target file the target file will be renamed to the new file name and kept in the same
        directory.
        TODO: 
        """
        if dir in self.directories:
            path = "./sounds/" + str(dir) + "/"  
            try:
                self.os.rename(path + str(oldFileName), path + str(newFileName) )
            except FileNotFoundError:
                print(path + str(oldFileName))
                print("file: " + str(oldFileName) + " not found")
            except FileExistsError: 
                print("file: " + str(newFileName) + " already exists")
        else:
            print("directory not found")

    def delete(self,dir,fileName):
        """
        This method will delete a specific file from a directory given directory and filename.

        TODO: 
         - tests
         - should we take directory as an arguemnt or the relative path to that file?
         - 
        """
        if dir in self.directories:
            path = "./sounds/" + str(dir) + "/" + str(fileName)
            try:
                self.os.remove(path)
            except FileNotFoundError:
                print("file" + str(fileName) + "not found in " + str(dir))
        else:
            print("directory not found")



    def add_file(self, fileOriginPath, fileDestPath):
        """
        
        NOTE: we do not need to do this for epoch one

        TODO:
        - should add file take an existing file and move it into a specific directory or 
        should it create a new file in a directory
        - test
        """
        raise NotImplementedError


    def list_files(self, dir):
        """
        NOTE: dir = name of directory NOT PATH

        This method will list all of the files in a directory or all subdirectories within the sounds directory
        default case is listing all the directories within the sound archive
         """
        files = []
        if (dir != "sounds") and (dir in self.directories): # path in case directory is specified
            path = "./sounds/" + str(dir) + "/"
        elif (dir == "sounds"): # path if directory is not specified
            path = "./sounds/"
        
        try:
            for file in os.listdir(path):
                files.append(file)
                print(file)
        except UnboundLocalError:
            print("file or directory not found")
        except FileNotFoundError:
            print("file or directory not found")
        return files

if __name__ == '__main__':
    pass