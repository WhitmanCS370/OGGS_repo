import argparse

class Interface():
    """
    attributes:
    parser : instance of the argparser ArguementParser
    arguements : added to object on parse_args stored as self."argname"

    methods:
    init_args : initializes the list of arguements that interface can recognize

    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.init_args()
        self.parser.parse_args(namespace = self)

    def init_args(self):
        self.parser.add_argument("-p", metavar="play",action = "extend",nargs = "+" ,help = "play sound file")
        self.parser.add_argument("-l", metavar="list", action = "store",help = "list sounds in directory")
        self.parser.add_argument("-rn", metavar="rename", action = "store", help = "rename sound")

    def play_file(self):
        pass

    def list_files(self):
        pass

    def rename_file(self):
        pass 