import sys
from audio import *

class Controller:
    """
    
    """
    def __init__(self,files):
        player=Player()
        for file in files:
            player.playsound(file)
        print("Controller")


class FileManager:
    """
    
    """
    def __init__(self):
        print("File Manager")
        
def main():
    if len(sys.argv)<=1 or sys.argv[1]=='--help' or sys.argv[1]=='-h':
        # This prints out a sample of how you might use this command
        print("usage:",sys.argv[0], '--help')

        help_message = """
        Usage: python cli_example.py [command] [arguments]
        Commands:
        -c, --count    : Count the number of arguments.
        -p, --play     : Play the specified sound file. Usage: -p <filepath>
        -h, --help     : Show this help message.
        """
        print(help_message)
        # Hygiene
        sys.exit(0)
    if sys.argv[1] == '-p' or sys.argv[1] == '--play' :
        Control=Controller(sys.argv[2:])
        sys.exit(0)
    
    if sys.argv[1]=='-c' or sys.argv[1]=='--count':
        return len(sys.argv)-2
            
            
    
if __name__ == '__main__':
    main()
