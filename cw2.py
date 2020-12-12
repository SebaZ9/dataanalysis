import sys
import GuiController
import ConsoleController

"""
Entry point of the program
Gui Usage: python cw2.py
To see command line usage : python cw2.py -h
"""

if len(sys.argv) == 1:
    GuiController.run()
else:
    ConsoleController.run_commands()
