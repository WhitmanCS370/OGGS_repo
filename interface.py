import cmd
from audio import AudioEffects
from manager import FileManager
from os import walk

class Interface(cmd.Cmd):
    """
    A command-line interface class using the cmd module.

    To add new command line arguements, add a method to this class with the prefix "do_" and the parameters self, args.
    args will be the arguements passed after the command and are interpreted as one string.
    do parsing of the string into parameters suitable for the necessary other method in it's appropriate "do_" method.
    """
    
    def __init__(self):
        super().__init__()
        self.intro = "Welcome to the audio library CLI, enter 'help' for a list of commands"
        self.prompt = ">>"
        self.audio = AudioEffects()
        self.files = FileManager()

    def provide_arg(self):
        print("*** please provide a valid arguement")
        print("*** type 'help' for list of commands")

    def validate_list_args(self, args, nArgs): 
        """
        validate that a given string args can be interpreted as list of nArgs length
        args: arguements to be validated
        nArgs: target length for arguement list
        """
        if (len(args.split()) != nArgs):
            return False
        return True
    
    def validate_single_arg(self, args):
        """
        validate that args is a single arguement, not a list
        args: arguements to be validated
        """
        if ((len(args.split()) > 1) or args == ""):
            return False
        return True

    def do_play(self, args):
        """
        Desc: Play a sound from the library.
        Usage: play <filepath>
        """
        if (self.validate_single_arg(args)):
            self.audio.play(args)
        else:
            self.provide_arg()

    def do_list(self, args):
        """
        Desc: List files in one of the library's directorys
        Usage: list <directoryName>
        """
        if (self.validate_single_arg(args)):
            self.files.list_files(args)
        else:
            self.provide_arg()

    def do_rename(self, args):
        """
        Desc: Rename sound in directory.
        Usage: rename <directory> <oldFilename> <newFilename>
        """
        if (self.validate_list_args(args=args, nArgs=3)):
            args = args.split()
            self.files.rename(args[0], args[1], args[2])
        else:
            self.provide_arg()

    def do_remove(self, args):
        """
        Desc: Delete sound in directory.
        Usage: delete <directory> <filename>
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.files.delete(args[0], args[1])
        else:
            self.provide_arg()

    def do_layer(self, args):
        """
        Desc: Play a list of files at the same time. 
        Usage: layer [filePath, ...]
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.audio.layer(args)
        else:
            self.provide_arg()

    def do_seq(self, args):
        """
        Desc: Play a list of files one after another. 
        Usage: seq [filePath, ...]
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.audio.sequence(args)
        else:
            self.provide_arg()

    def do_exit(self, args):
        """
        Desc: Exit the interface.
        Usage: exit
        """
        return True

if __name__ == "__main__":
    CLI_interface = Interface()
    CLI_interface.cmdloop()
