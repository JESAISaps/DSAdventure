import sys
import time
import questionary
import msvcrt

def flush_stdin():
    while msvcrt.kbhit():
        msvcrt.getch()

name = questionary.text("What's your name?").ask()
time.sleep(2)
flush_stdin()
age = questionary.text("How old are you?").ask()