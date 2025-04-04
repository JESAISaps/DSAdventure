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

    def PaintRoom(self):
        return r"""
########################################################################
#                          ______   __                                 #
#                          /      \ /  |                               #
#   1) Stylo - 10         /$$$$$$  |$$ |____    ______    ______       #
#   2) Chaussettes - 5    $$ \__$$/ $$      \  /      \  /      \      #
#   3) Gomme - 7          $$      \ $$$$$$$  |/$$$$$$  |/$$$$$$  |     #
#   4) Blanco - 4          $$$$$$  |$$ |  $$ |$$ |  $$ |$$ |  $$ |     #
#                         /  \__$$ |$$ |  $$ |$$ \__$$ |$$ |__$$ |     #
#                         $$    $$/ $$ |  $$ |$$    $$/ $$    $$/      #
#                          $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$/       #
#                                                       $$ |           #
#                                                       $$ |           #
#                                                       $$/            #
########################################################################
"""


class Menu(Room):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def RoomIntroduction(self):
        return f"Bienvenue dans l'accueil nommé {self._name} !"
    
class Shop(Room):
    def __init__(self, name):
        super().__init__()
        self._name=name

    def RoomIntroduction(self):
        return f"Bienvenue au {self._name} !"
    
    def PaintRoom(self):
        return r"""
########################################################################
#                          ______   __                                 #
#                          /      \ /  |                               #
#   1) Stylo - 10         /$$$$$$  |$$ |____    ______    ______       #
#   2) Chaussettes - 5    $$ \__$$/ $$      \  /      \  /      \      #
#   3) Gomme - 7          $$      \ $$$$$$$  |/$$$$$$  |/$$$$$$  |     #
#   4) Blanco - 4          $$$$$$  |$$ |  $$ |$$ |  $$ |$$ |  $$ |     #
#                         /  \__$$ |$$ |  $$ |$$ \__$$ |$$ |__$$ |     #
#                         $$    $$/ $$ |  $$ |$$    $$/ $$    $$/      #
#                          $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$/       #
#                                                       $$ |           #
#                                                       $$ |           #
#                                                       $$/            #
########################################################################
"""

class FightRoom(Room):
    def __init__(self, ennemies:list):
        self._enemies = ennemies
        self._nbEnemies = len(ennemies)
        super().__init__()

    def RoomIntroduction(self):
        return f"Tu arrive en face de {self._nbEnemies} ennemis"
    
    def GetEnemiNb(self):
        return self._nbEnemies()

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
        return r"""
   ___         _       _  _                
  / __|___  __| |___  | \| |__ _ _ __  ___ 
 | (__/ _ \/ _` / -_) | .` / _` | '  \/ -_)
  \___\___/\__,_\___| |_|\_\__,_|_|_|_\___|                                                                       
"""

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
            return True
        else:
            print("Erreur, c'est votre dernière chance")
            if self.StartManche():
                print("Bravo, vous avez gagné un Talisman")
                return True
            else : 
                print("Vous n'avez rien gagné")
            
class Morpion(DefiRoom):
    def __init__(self):
        super().__init__("Morpion")
        self.matrice=[[" "," "," ",],[" "," "," "],[" "," "," "]]
        self.dico={"A1":[0][0],"A2":"[0][1]","A3":"[0][2]","B1":"[1][0]","B2":"[1][1]","B3":"[1][2]","C1":"[2][0]","C2":"[2][1]","C3":"[2][2]"}


    def ShowMatrice(self):
        rep=""
        rep+="    1   2   3"
        for i in range(3):
            rep+=f"\n {chr(65+i)}  {self.matrice[i][0]} | {self.matrice[i][1]} | {self.matrice[i][2]} \n   -----------"
        print(rep[:-11])


    def MancheJoueur(self):
        pass

    def AskChoice(self):
        rep = click.prompt("Quelle case souhaitez vous jouer?",type=CustomChoice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], case_sensitive=False), show_choices=False).upper()
        verif=self.dico[rep]
        print(verif)
        if self.matrice[verif] !=[" "]:
            print("Erreur la case est déjà utilisée")
        else:
            print(rep)

    def ModifierMatrice(self, choix):
        match choix :
            case "A1" : self.matrice[0][0]="x"
            case "A2" : self.matrice[0][1]="x"
            case "A3" : self.matrice[0][2]="x"
            case "B1" : self.matrice[1][0]="x"
            case "B2" : self.matrice[1][1]="x"
            case "B3" : self.matrice[1][2]="x"
            case "C1" : self.matrice[2][0]="x"
            case "C2" : self.matrice[2][1]="x"
            case "C3" : self.matrice[2][2]="x"
            case _ : print("ERREUR")
    
    def ComputerTour(self):
        return random(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])



if __name__ == "__main__":
    morpion = Morpion()
    #codeName = DefiRoom("codeName")
    #sphinx = DefiRoom("sphinx")
    #integrale = DefiRoom("intégrale")
    
    #code=CodeName()
    #print(code.RoomIntroduction())
    #code.StartGame()
    morpion.ShowMatrice()
    morpion.AskChoice()

    #shop=Shop("Shop")
    #print(shop.PaintRoom())

