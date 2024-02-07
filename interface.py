import sys

class interface():
    def __init__(self) -> None:
        self.help_message = """
        Usage: python cli_example.py [command] [arguments]
        Commands:
        -c, --count    : Count the number of arguments.
        -p, --play     : Play the specified sound file. Usage: -p <filepath>
        -h, --help     : Show this help message.
        """
        
        
    def play():
        pass

    def help(self):
        print(self.help_message)
    
    