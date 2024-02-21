import argparse
from audio import * 
from manager import FileManager
import os
from os import walk
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
        self.init_tools()
        self.parser.parse_args(namespace = self)
        
    def init_tools(self):
        self.audio = AudioEffects()
        self.files = FileManager()

    def init_parser(self):
        """
        initialize the arguement parser
        """
        self.parser = argparse.ArgumentParser()
        self.init_args()

    def init_args(self):
        """
        initializes list of commands for CLI
        -h and --help list all of the optional commands
        
        If you need to add a new command line arguement, add it here
            first two args are the specific command string
            metavar: is the variable that the args will be stored under as self."metavar"
            action: is how the arg is handled, extend stores args as list, store just stores verbaitm
            help: is the help text associated with the command

        TODO:
         - is there a better way to add arguements? 
        """
        self.parser.add_argument("-p","--play",metavar="play" ,help = "play sound ")
        self.parser.add_argument("-l","--list",metavar="list",action = "store",nargs="?",help = "Lists files in directory, usage: -l <directory name>")
        self.parser.add_argument("-rn","--rename",metavar="rename",action = "extend",nargs="+", help = "Renames sound in directory, usage: -rn <directory name> <target filename> <new filename>")
        self.parser.add_argument("-rm","--remove",metavar="remove",action = "extend",nargs="+", help = "Deletes sound in directory, usage: -rm <directory name> <target filename>")
        self.parser.add_argument("-ly","--layer", metavar="layer", action="extend",nargs="+",help="layer the audio")
        self.parser.add_argument("-sq","--sequence",metavar="sequence", action="extend",nargs="+",help="sequences one sound after another")
        
#-l 
    def delegate_args(self):
        """
        this method is meant to delegate arguements to the corrosponding objects
        """
        if (self.play):
            AudioEffect=AudioEffects()
            AudioEffect.play(self.get_play_args())
            
        if (self.list):
            file_manager = FileManager()
            file_manager.list_files(self.list)

        if (self.rename):
            file_manager = FileManager()
            file_manager.rename(self.rename[0], self.rename[1], self.rename[2])
            
        if (self.remove):
            file_manager = FileManager()
            file_manager.delete(self.remove[0], self.remove[1])
            
        if(self.layer):
            AudioEffect=AudioEffects()
            AudioEffect.layer(self.get_layer_args())
        
        if(self.sequence):
            AudioEffect=AudioEffects()
            AudioEffect.sequence(self.get_sequence_args())
    
    def get_play_args(self):
        """
        return the arguemnts passed in with the -p command
        """
        return self.play

    def get_list_args(self):
        """
        handle args for the list command
        """
        pass

    def get_rename_args(self):
        """
        returns the arguements passed in with the -rn command
        """
        return self.rename
    
    def get_layer_args(self):
        """
        returns the arguements passed in with the -ly command
        """
        l=[]
        if self.layer==None:
            return None
        for item in self.layer:
            if os.path.isfile(item):
                l.append(item)
            elif os.path.isdir(self.layer[0]):
                for (dir_path,dir,files) in walk(item):
                    for file in files:
                        if file.endswith(".wav"):
                            l.append('./'+dir_path+'/'+file)
        return l
    
    def get_sequence_args(self):
        """
        returns the arguements passed in with the -seq command
        """
        l=[]
        if self.sequence==None:
            return None
        for item in self.sequence:
            if os.path.isfile(item):
                l.append(item)
            elif os.path.isdir(self.sequence[0]):
                for (dir_path,dir,files) in walk(item):
                    for file in files:
                        if file.endswith('.wav'):
                            l.append('./'+dir_path+'/'+file)
        return l
    
    def delegate(self,type):
        """
        should delegate the arguments that were recieved and parsed to their individual class so that they can run them

        Args:
            type:
        """
        return type

if __name__ == "__main__":
    CLI_interface = Interface()
    CLI_interface.delegate_args()