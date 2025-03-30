from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self):
        self._voisin = {}

    @abstractmethod
    def RoomIntroduction(self):
        pass

    def GetVoisins(self):
        return self._voisin
    
    def SetVoisins(self, nord=None, sud=None, est=None, ouest=None):
        self._voisin["Nord"] = nord
        self._voisin["Sud"] = sud
        self._voisin["Est"] = est
        self._voisin["Ouest"] = ouest


class Menu(Room):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def RoomIntroduction(self):
        return f"Bienvenue dans l'accueil nomé {self._name} !"

class FightRoom(Room):
    def __init__(self, ennemies:list):
        self._enemies = ennemies
        self._nbEnemies = len(ennemies)
        super().__init__()

    def RoomIntroduction(self):
        return f"Tu arrive en face de {self._nbEnemies} ennemis"

class DefiRoom(Room):
    def __init__(self, name):
        self._name = name
    
    def RoomIntroduction(self):
        return f"Super, un peu de repos, tu arrives dans la salle {self._name}"

if __name__ == "__main__":
    morpion = DefiRoom()
    codeName = DefiRoom()
    sphinx = DefiRoom()
    integrale = DefiRoom()


