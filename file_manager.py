import sys
import os

class FileManager():
    def __init__(self):
        pass

    def rename(self, oldFile, newFile):
        try:
            os.rename(oldFile, newFile)
        except FileNotFoundError:
            print("file: " + str(oldFile) + "not found")
        except FileExistsError: 
            print("file: " + str(newFile) + " already exists")


    def delete(self, fileName):
        try:
            os.remove(fileName)
        except FileNotFoundError:
            print("file" + str(fileName) + "not found")

    def add_file(self, filePath, dest):
        pass

    def list_files(self, dest):
        pass

