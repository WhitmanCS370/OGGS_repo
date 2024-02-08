import argparse

class Interface():
    """
    attributes:
    parser : instance of the argparser ArguementParser
    arguements : added to object on parse_args stored as self."argname"

    methods:
    init_args : initializes the list of arguements that interface can recognize
    init_parser : initializes the arguement parser
    """
    def __init__(self):
        self.init_parser()
        self.parser.parse_args(namespace = self)

    def init_parser(self):
        """
        initialize the arguement parser
        """
        self.parser = argparse.ArgumentParser()
        self.init_args()

    def init_args(self):
        """
        initializes list of commands for CLI
        """
        self.parser.add_argument("-p","--play",metavar="play",action = "extend", nargs = "+" ,help = "play sound ")
        self.parser.add_argument("-l","--list",metavar="list",action = "store",help = "list sounds in directory")
        self.parser.add_argument("-rn","--rename",metavar="rename",action = "store", help = "rename sound")

    def play_file(self):
        """
        placeholder
        """
        pass

    def list_files(self):
        """
        placeholder
        """
        pass

    def rename_file(self):
        """
        placeholder
        """
        pass 

interface = Interface()

interface