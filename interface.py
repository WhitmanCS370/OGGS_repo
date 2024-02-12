import argparse

class Interface():
    """
    attributes:
    parser : instance of the argparser ArguementParser
    arguements : added to object on parse_args stored as self."argname", not listed on intialization

    methods:
    init_args : initializes the list of arguements that interface can recognize
    init_parser : initializes the arguement parser
    """
    def __init__(self):


        self.init_parser()
        self.parser.parse_args(namespace = self)

        #self.play # these attributes are created on call of parse_args
        #self.list
        #self.rename

    def init_parser(self):
        """
        initialize the arguement parser
        """
        self.parser = argparse.ArgumentParser()
        self.init_args()

    def init_args(self):
        """
        initializes list of commands for CLI

        If you need to add a new command line arguement, add it here
            first two args are the specific command string
            metavar is the variable that the args will be stored under as self."metavar"
            action is how the arg is handled, extend stores args as list, store just stores verbaitm
            help is the help text associated with the command

        TODO:
         - is there a better way to add arguements? 
        """
        self.parser.add_argument("-p","--play",metavar="play",action = "extend", nargs = "+" ,help = "play sound ")
        self.parser.add_argument("-l","--list",metavar="list",action = "store",help = "list sounds in directory")
        self.parser.add_argument("-rn","--rename",metavar="rename",action = "store", help = "rename sound")

    def get_play_args(self):
        """
        return the arguemnts passed in with the -p command
        """
        return self.play

    def get_list_args(self):
        """
        return the arguements passed in with the -l command
        """
        return self.list
    
    def get_rename_args(self):

        """
        returns the arguements passed in with the -rn command
        """
        return self.rename


interface = Interface()

interface