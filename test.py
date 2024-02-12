import unittest
import os
from manager import *
from audio import *



class Test(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """
    def test_Playing(self):
        print("test")



class FileManager_test(unittest.TestCase):
    """
    test funtctionality of the FileManager
    """
    def __init__(self):
        self.file_manager = FileManager()

    def test_rename(self):
        """
        TODO: 
            - rename test file
            - assert that that file exists in the directory
            - rename back to test file
        """
        

    def test_delete():
        """
        TODO: 
            - add file
            - assert that file exists
            - delete that file
            - assert that file does not exist 
        """

    def test_list_files():
        pass




if __name__ == "__main__":
    unittest.main()