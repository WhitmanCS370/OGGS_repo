import sys
import os
from audio import *

class FileManager():
    def __init__(self):
        self.os = os
        self.directories = self.os.listdir("./sounds/")

    def rename(self, dir, oldFile, newFile):

        """
        This method will take in a target directory, target file, and a new file name for the
        target file the target file will be renamed to the new file name and kept in the same
        directory.

        TODO: 

        """
        if dir in self.directories:
            path = "./sounds/" + str(dir) + "/"  
            try:
                self.os.rename(path + str(oldFile), path + str(newFile) )
            except FileNotFoundError:
                print(path + str(oldFile))
                print("file: " + str(oldFile) + " not found")
            except FileExistsError: 
                print("file: " + str(newFile) + " already exists")
        else:
            print("directory not found")



    def delete(self,dir, fileName):
        """
        This method will delete a specific file from a directory given the path to that file.


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
                print("file" + str(fileName) + "not found")
        else:
            print("directory not found")



    def add_file(self, filePath, dest):
        pass

    def list_files(self, dest):
        pass
        
def main():

    filemanager = FileManager()

    filemanager.rename("old-sounds", "toaster.wav", "toaster.wav")

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
