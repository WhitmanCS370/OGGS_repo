import cmd
from audio import AudioEffects
from audio import Recorder
from manager import FileManager
from sql_commands import databaseManager
from database_init import init
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
        self.prompt = ">> "
        self.audio = AudioEffects()
        self.files = FileManager()
        init()
        self.recorder=Recorder()
        self.db = databaseManager()
        #for development purposes, populate database with example files
        self.db.add_all()

    def provide_arg_msg(self):
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
        Usage: play <filename>
        """
        if (self.validate_single_arg(args)):
            self.audio.set_currently_playing_file(self.db.get_filepath(args))
            self.audio.play()
        else:
            self.provide_arg_msg()

    def do_resume(self, args):
        """
        Desc: Resume a paused sound.
        Usage: resume
        """
        self.audio.resume()

    # def do_list(self, args):
    #     """
    #     Desc: List files in one of the library's directorys
    #     Usage: list <directoryName>
    #     """
    #     if (self.validate_single_arg(args)):
    #         self.files.list_files(args)
    #     else:
    #         self.provide_arg_msg()

    # def do_rename(self, args):
    #     """
    #     Desc: Rename sound in directory.
    #     Usage: rename <directory> <oldFilename> <newFilename>
    #     """
    #     if (self.validate_list_args(args=args, nArgs=3)):
    #         args = args.split()
    #         self.files.rename(args[0], args[1], args[2])
    #     else:
    #         self.provide_arg_msg()

    # def do_remove(self, args):
    #     """
    #     Desc: Delete sound in directory.
    #     Usage: delete <directory> <filename>
    #     """
    #     if (self.validate_list_args(args=args, nArgs=2)):
    #         args = args.split()
    #         self.files.delete(args[0], args[1])
    #     else:
    #         self.provide_arg_msg()

    def do_layer(self, args):
        """
        Desc: Play a list of files at the same time. 
        Usage: layer [filePath, ...]
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.audio.layer(args)
        else:
            self.provide_arg_msg()

    def do_seq(self, args):
        """
        Desc: Play a list of files one after another. 
        Usage: seq [filePath, ...]
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.audio.sequence(args)
        else:
            self.provide_arg_msg()

    def do_new_playlist(self, args):
        """
        Desc: Add a playlist to the database.
        Usage: new_playlist <playlistName>
        """
        if (self.validate_single_arg(args)):
            self.db.add_playlist(args)
        else:
            self.provide_arg_msg()

    def do_playlist_add(self, args):
        """
        Desc: Add a song to a playlist.
        Usage: playlist_add <playlistName> <songName>
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.db.song_to_playlist(args[0], args[1])
        else:
            self.provide_arg_msg()
    
    def do_list_playlists(self, args):
        """
        Desc: Show all playlists in the database.
        Usage: show_playlists
        """
        playlists = list(self.db.list_playlists())
        self.columnize(playlists)
        # for playlist in playlists:
        #     print(playlist[0])


    def do_list_files(self, args):
        """
        Desc: Show all files database
        Usage: show_all
        """
        files = list(self.db.list_files())
        self.columnize(files)
        # for file in files:
        #     print(file[0])

    def do_new_tag(self, args):
        """
        Desc: Add a tag to the database.
        Usage: add_tag <tagName> <tagDesc>
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.db.add_tag(args[0], args[1])
        else:
            self.provide_arg_msg()


    def do_tag_add(self, args):
        """
        Desc: Add a tag to a song.
        Usage: tag_add <tagName> <songName>
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.db.add_tag_to_file(args[0], args[1])
        else:
            self.provide_arg_msg()

    def do_list_tag(self, tag):
        """
        Desc: Show all files with a given tag.
        Usage: show_tag <tagName>
        """
        files = list(self.db.get_from_tag(tag))
        self.columnize(files)
        # print(files)
        # for file in files:
        #     print(file[1])
    
    def do_rename(self, args):
        """
        Desc: Rename a file in the archive
        Usage: rename <oldFileName> <newFileName>
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.files.rename(args[0], args[1])
        else:
            self.provide_arg_msg()

    def do_list_tags(self, args):
        """
        Desc: List all tags in the database.
        Usage: list_tags
        """
        tags = list(self.db.list_tags())
        self.columnize(tags)
        # for tag in tags:
        #     print(tag[0])

    def do_exit(self, args):
        """
        Desc: Exit the interface.
        Usage: exit
        """
        return True
    def do_rec(self,args):
        """
        Desc: start recording and wait for keyboard input to stop
        Usage: rec
        """
        self.recorder.record()
        
    def do_record(self, args="NoArgs"):
        """
        Desc: start recording and wait for keyboard input to stop
        Usage: record [filepath/name]
        """
        
        if (self.validate_single_arg(args=args)):
            self.recorder.record(args)
        else:
            self.provide_arg_msg()
    


if __name__ == "__main__":
    CLI_interface = Interface()
    CLI_interface.cmdloop()
