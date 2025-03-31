from abc import ABC, abstractmethod
import click 
import questionary
import random
from Utils import * 

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
        return f"Bienvenue dans l'accueil nommé {self._name} !"

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
    
class CodeName(DefiRoom):
    def __init__(self):
        super().__init__("Code Name")
        self.liste = [("police",("girophare","enfermer")),("barcelo",("cheveux","mathématiques"))]
        self.tupleJeu=self.liste.pop()

    def RoomIntroduction(self):
        print("""   
   ___         _       _  _                
  / __|___  __| |___  | \| |__ _ _ __  ___ 
 | (__/ _ \/ _` / -_) | .` / _` | '  \/ -_)
  \___\___/\__,_\___| |_|\_\__,_|_|_|_\___|                                                                       
                                                                          """)

    def AskQuestion(self):
        print(f"Je te donne 2 mots : {self.tupleJeu[1][0]} et {self.tupleJeu[1][1]}")
    
    def GetAnswer(self):
        reponse=click.prompt("A quoi je pense?", type=str)
        return reponse

    def Verification(self, reponse):
        if self.liste==[]:
            print("Jeu fini")
        return CompareWord(reponse,self.tupleJeu[0])
    
    def StartManche(self):
        self.AskQuestion()
        reponse = self.GetAnswer()
        return self.Verification(reponse)
        
    def StartGame(self):
        print(f"On commence le {self._name}")
        if self.StartManche()==True:
            print("Bravo, vous avez gagné un Talisman")
            return True #TODo Ajouter Talisman
        else:
            print("Erreur, c'est votre dernière chance")
            if self.StartManche():
                print("Bravo, vous avez gagné un Talisman")
                return True #AJOUTER UN TALISMAN TODO
            else : 
                print("Vous n'avez rien gagné")
            



if __name__ == "__main__":
    morpion = DefiRoom("morpion")
    codeName = DefiRoom("codeName")
    sphinx = DefiRoom("sphinx")
    integrale = DefiRoom("intégrale")
    
    code=CodeName()
    code.StartGame()