from gui import open_gui
from interface import Interface
from sys import argv

if (__name__ == "__main__"):
    if "-g" in argv:
        open_gui()
    else:
        i = Interface()
        i.cmdloop()