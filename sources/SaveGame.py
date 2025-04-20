from Player import Player
from Object import Armure, Arme
from Utils import ObjectType

try:
    import _pickle as pickle
except:
    import pickle



def SaveGame(player:Player):
    try:
        with open("saved_game.pkl", "rb") as file:
            dico = pickle.load(file)
    except FileNotFoundError:
        dico = {}
    dico[player.GetName()] = player
    with open("saved_game.pkl", "wb") as file:
        pickle.dump(dico, file, -1)

def LoadGame() -> dict[Player]:
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