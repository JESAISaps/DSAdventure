from Player import Player
import click
from Room import DefiRoom, FightRoom, Menu, Shop
import questionary
import keyboard

player = Player("Jean", 0)


isQPressed = False
presse = keyboard.read_hotkey()
print(presse)