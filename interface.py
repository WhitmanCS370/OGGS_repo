import cmd
from audio import AudioEffects, Recorder
from file_system import FileManager
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
    
    def do_add_all(self, args):
        """
        Desc: Add all files in the sounds directory to the database.
        Used only for initialization.
        Usage: add_all
        """
        confirmation = ""
        while confirmation.lower() not in ["y","n"]:
            confirmation = input("adding all existing files to database, Y/N? ")
            if confirmation.lower() == "y":
                print("adding all files: \n--------------------")
                self.db.add_all()
                print("--------------------\nall files added to database.")
    
    def do_play(self, args):
        """
        Desc: Play a sound from the library.
        Usage: play <filename>
               play -p <playlist_name>
        """
        if args.split()[0] == "-p":
            if (self.validate_list_args(args, 2)):
                files = self.db.get_playlist(args.split()[1])
                if any(files):
                    for file in files:
                        self.audio.set_currently_playing_file(file)
                        self.audio.play()
        else:
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

    def do_layer(self, args):
        """
        Desc: Play a list of files at the same time. 
        Usage: layer [filePath, ...]
        """
        if (self.validate_list_args(args=args, nArgs=2)):
            args = args.split()
            self.audio.layer(self.db.get_filepath(args[0]),self.db.get_filepath(args[1]))
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

    def do_show_playlist(self, args):
        """
        Desc: Show the files in a playlist
        Usage: show_playlist <playlist_name>
        """
        if self.validate_single_arg(args):
            songs = self.db.show_playlist(args)
            self.columnize(songs)


    def do_list_files(self, args):
        """
        Desc: Show all files database
        Usage: show_all
        """
        files = list(self.db.list_files())
        self.columnize(files)

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


    def do_add_tag(self, args):
        """
        Desc: Add a tag to a song.
        Usage: add_tag <tagName> <songName>
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
        
    def do_record(self,args):
        """
        Desc: starret recording and wait for keyboard input to stop
        Usage: record [name of new file]
        """
        if (self.validate_single_arg(args=args)):
            self.recorder.record(args)
        else:
            self.provide_arg_msg()
            
    def do_check_inputs(self,args):
        """
        Desc: start recording and wait for keyboard input to stop
        Usage: record [name of new file]
        """
        self.recorder.check_inputs()
    
    def do_duplicate_file(self,args):
        """
        Desc: duplicate the specified file
        Usage: duplicate_file [name of new file]
        """
        if (self.validate_single_arg(args=args)):
            self.files.duplicate_file(args,self.db)
        else:
            self.provide_arg_msg()
            
    def do_speed_up(self,args):
        """
        Desc: speed up file by specified amount
        Usage: speed [name of new file] [sped up amount]
        """
        if (self.validate_list_args(args=args,nArgs=2)):
            args=args.split()
            filename = self.db.get_filepath(args[0])
            new_file = self.audio.speed_up(filename, args[1])
            self.db.add_from_file(new_file)
        else: 
            self.provide_arg_msg()
    
    def do_trim(self,args):
        """
        Desc: trims off the start and end of the .wav file
        Usage: trim [name of new file] startTimeStamp endTimeStamp
        """
        if (self.validate_list_args(args=args,nArgs=3)):
            args=args.split()
            filename = self.db.get_filepath(args[0])
            new_file = self.audio.trim(filename,args[1],args[2])
            self.db.add_from_file(new_file)
        else: 
            self.provide_arg_msg()
            
    def do_backward(self,args):
        """
        Desc: reverses the selected file and saves to a new audio file
        Usage: backward <filename>
        """
        if (self.validate_single_arg(args=args)):
            filepath = self.db.get_filepath(args)
            new_file = str(self.audio.backward(filepath))
            self.db.add_from_file(new_file)
        else: 
            self.provide_arg_msg()
    
    def do_check_length(self,args):
        """
            Desc: checks to see how long the file is in milliseconds
            Usage: check_lenght <filename>
        """
        if (self.validate_single_arg(args=args)):
            filename = self.db.get_filepath(args)
            duration = self.audio.check_length(filename)
            print(f'{args} is {duration} seconds long')
        else: 
            self.provide_arg_msg()

if __name__ == "__main__":
    CLI_interface = Interface()
    CLI_interface.cmdloop()
