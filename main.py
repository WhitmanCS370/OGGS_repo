from gui import gui
from interface import Interface
from sys import argv

if (__name__ == "__main__"):
    if "-g" in argv:
        i = gui()
    else:
        i = Interface()
        i.cmdloop()