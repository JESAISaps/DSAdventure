from Player import Player
import click
from Room import DefiRoom, FightRoom, Menu
import questionary
import keyboard

player = Player("Jean", 0)

firstRoom = Menu("Hehe")

actualRoom = firstRoom

print(actualRoom.RoomIntroduction())
print("Que veux tu faire")

#hehe = click.prompt("Quelle salle", type=int, show_choices=True)


question = questionary.select(
    "What do you want to do?",
    choices=[
        'Order a pizza',
        'Make a reservation',
        'Ask for opening hours'
    ])

question.ask()

isQPressed = False
presse = keyboard.read_hotkey()
print(presse)