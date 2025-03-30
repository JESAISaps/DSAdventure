from Player import Player
import click
from Room import DefiRoom, FightRoom, Menu

player = Player("Jean", 0)

firstRoom = Menu("Hehe")

actualRoom = firstRoom

print(actualRoom.RoomIntroduction())
print("Que veux tu faire")

hehe = click.prompt("Quelle salle", type=int, show_choices=True)
