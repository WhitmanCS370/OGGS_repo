import cmd
import os
from audio_pyaudio import AudioPlayer
from file_system import FileManager
from sql_commands import databaseManager
from database_init import init

class Interface(cmd.Cmd):
    """
    Seperate implementation of CLI using pyaudio instead of pydubs,
    as pydubs has issues on Windows.
    """
    def __init__(self):
        super().__init__()
        self.intro = "Welcome to the audio library CLI, enter 'help' for a list of commands"
        self.prompt = ">> "
        self.player = AudioPlayer
        self.files = FileManager()
        self.db = databaseManager()
        self.db_init = init

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
    
    def do_database_init(self, args):
        """
        Desc: Initialize or reset the database. Use with caution.
        Usate: database_init
        """
        confirmation = ""
        while confirmation.lower() not in ["y","n"]:
            confirmation = input("resetting database, Y/N? ")
            if confirmation.lower() == "y":
                print("resetting database: \n--------------------")
                self.db_init()
                print("--------------------\ndatabase reinitialized.")
            elif confirmation.lower() == "n":
                print("cancelling operation.")
                break
            else:
                print("please provide valid argument")

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
    
    # Streaming functions ----------

    def do_play(self, args):
        """
        Desc: Play a sound from the library.
        Usage: play <filename>
        """
        if not self.validate_single_arg(args):
            self.provide_arg_msg()
            return

        filepath = self.db.get_filepath(args)  # Assume this method returns a valid path or None
        if filepath is None:
            print(f"No audio file found for: {args}")
            return

        try:
            self.player = AudioPlayer(filepath)
            self.player.play()
            print("Playback started. Type 'pause' to pause, 'resume' to resume, or 'stop' to stop.")
        except Exception as e:
            print(f"Failed to start playback: {e}")

    def do_pause(self, args):
        """ Pause the currently playing sound. """
        if hasattr(self, 'player') and self.player:
            try:
                self.player.pause()
                print("Playback paused.")
            except Exception as e:
                print(f"Failed to pause playback: {e}")
        else:
            print("No sound is currently playing.")

    def do_resume(self, args):
        """ Resume the currently paused sound. """
        if hasattr(self, 'player') and self.player:
            try:
                self.player.resume()
                print("Playback resumed.")
            except Exception as e:
                print(f"Failed to resume playback: {e}")
        else:
            print("No sound is currently paused.")

    def do_stop(self, args):
        """ Stop the currently playing sound. """
        if hasattr(self, 'player') and self.player:
            try:
                self.player.stop()
                print("Playback stopped.")
            except Exception as e:
                print(f"Failed to stop playback: {e}")
        else:
            print("No sound is currently playing.")

    def do_reset(self, args):
        """ Reset the currently playing sound. """
        if hasattr(self, 'player') and self.player:
            try:
                self.player.reset()
                print("Playback reset.")
            except Exception as e:
                print(f"Failed to reset playback: {e}")
        else:
            print("No sound is currently playing.")
    
    def do_skip(self, args):
        """skip to a timeframe"""
        if hasattr(self, 'player') and self.player:
            try:
                self.player.skip_to(args)
                print(f"skipped to {args}")
            except Exception as e:
                print(f"Failed to skip to timeframe{args}, error: {e}")

if __name__ == "__main__":
    CLI_interface = Interface()
    CLI_interface.cmdloop()