import sys
import simpleaudio as sa

def play_sound(filename):
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

'''
# HELP: This is a command line argument that is invoked by typing --help or -h
(Note that it is a command line convention to offer full name and first letter options.
The full name options have two preceding dashes -- and the one-letter options have just one -)
For example:
>> python cli_example.py --help
>> python cli_example.py --h
Right now, this help command is not very useful.
Take a look at some other helps commands, like
>> python --help
>> pip -h
>> conda --help
To see what they include.
'''

# This if statement checks to see what argument comes right after the program name
# Note that it also runs if you have no arguments after the program name
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
    for filename in sys.argv[2:]:
        play_sound(filename)
    sys.exit(0)


"""
possible restructure to accept commands after running the program rather than just on initial 
command line arguements
"""