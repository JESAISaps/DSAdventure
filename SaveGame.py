from Player import Player
from Object import Armure, Arme
from Utils import ObjectType

import _pickle as pickle



def SaveGame(player:Player):
    with open("saved_game.pkl", "wb") as file:
        pickle.dump(player, file, -1)

def LoadGame() -> Player:
    try:
        with open("saved_game.pkl", "rb") as file:
            toReturn = pickle.load(file)
        return toReturn
    except FileNotFoundError:
        return False
    

if __name__ == "__main__":
    player = Player("caca", 10, 10, 10)
    chapeau = Armure("rrrr", ObjectType.Chapeau, 10)
    arme = Arme("tttt", ObjectType.Arme, 0,20)
    player.AddItem(chapeau)
    player.AddItem(arme)

    player.EquipItem(chapeau)
    player.EquipItem(arme)

    SaveGame(player)
    del player

    print(LoadGame())