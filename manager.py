import sys
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
            path = "./sounds/" + str(dir) + "/" 
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
        pass


    def list_files(self, dir = "sounds"):
        """
        NOTE: dir = name of directory NOT PATH

        This method will list all of the files in a directory or all subdirectories within the sounds directory
        default case is listing all the directories within the sound archive
         """
        
        if (dir != "sounds") and (dir in self.directories): # path in case directory is specified
            path = "./sounds/" + str(dir) + "/"
        elif (dir == "sounds"): # path if directory is not specified
            path = "./sounds/"
        
        try:
            for file in os.listdir(path):
                print(file)
        except UnboundLocalError:
            print("file or directory not found")
        except FileNotFoundError:
            print("file or directory not found")



        
        





        
def main():

    filemanager = FileManager()

    filemanager.add_file("~/Desktop/coffee-slurp-3.wav","~/Documents/GitHub/OGGS_repo/sounds/old-sounds/coffee-slurp-3.wav")

    # if len(sys.argv)<=1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':
    #     # This prints out a sample of how you might use this command
    #     print("usage:",sys.argv[0], '--help')

    #     help_message = """
    #     Usage: python cli_example.py [command] [arguments]
    #     Commands:
    #     -c, --count    : Count the number of arguments.
    #     -p, --play     : Play the specified sound file. Usage: -p <filepath>
    #     -h, --help     : Show this help message.
    #     """
    #     print(help_message)
    #     # Hygiene
    #     sys.exit(0)
    # if sys.argv[1] == '-p' or sys.argv[1] == '--play' :
    #     Control=Controller(sys.argv[2:])
    #     sys.exit(0)
    
    # if sys.argv[1]=='-c' or sys.argv[1]=='--count':
    #     return len(sys.argv)-2
            
            
    
if __name__ == '__main__':
    main()
