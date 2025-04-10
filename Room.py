from abc import ABC, abstractmethod
import click 
import questionary
import random
from Utils import * 
from sympy import integrate, symbols, oo, exp, ln, pprint, init_printing, latex, Integral
import matplotlib.pyplot as plt
from Player import Enemi, Player
from Combat import Fight

class Room(ABC):
    def __init__(self):
        self._voisin = {}

    @abstractmethod
    def RoomIntroduction(self):
        pass

    def GetVoisins(self):
        return self._voisin
    
    def SetVoisins(self, nord=None, sud=None, est=None, ouest=None, passage=None):
        self._voisin["Nord"] = nord
        self._voisin["Sud"] = sud
        self._voisin["Est"] = est
        self._voisin["Ouest"] = ouest
        self._voisin["passage"] = passage

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
    
    def PaintRoom(self):
        return r"""
  __  __              
 |  \/  |___ _ _ _  _ 
 | |\/| / -_) ' \ || |
 |_|  |_\___|_||_\_,_|

"""
    
class Conseil(Room):
    def __init__(self):
        super().__init__()
    
    def RoomIntroduction(self):
        return "Tu veux un bon conseil ? Bah non."
    
class Shop(Room):
    def __init__(self, name):
        super().__init__()
        self._name=name
        self._objects=[("Gomme", 5),("Bouteille d'eau", 8)]

    def RoomIntroduction(self):
        return f"Bienvenue au {self._name} !"
    
    def ShowObjects(self):
        print(f"Voici les objets de la boutique : {self._objects}")
    
    def PaintRoom(self):
        return r"""
########################################################################
#                  ______   __                                         #
#                  /      \ /  |                                       #
#                 /$$$$$$  |$$ |____    ______    ______               #
#                 $$ \__$$/ $$      \  /      \  /      \              #
#                 $$      \ $$$$$$$  |/$$$$$$  |/$$$$$$  |             #
#                  $$$$$$  |$$ |  $$ |$$ |  $$ |$$ |  $$ |             #
#                 /  \__$$ |$$ |  $$ |$$ \__$$ |$$ |__$$ |             #
#                 $$    $$/ $$ |  $$ |$$    $$/ $$    $$/              #
#                  $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$/               #
#                                               $$ |                   #
#                                               $$ |                   #
#                                               $$/                    #
########################################################################
"""

class FightRoom(Room):
    def __init__(self, ennemies:list[Enemi]):
        self._enemies = ennemies
        self._nbEnemies = len(ennemies)
        super().__init__()

    def StartFight(self, player):
        fight = Fight(player, self._enemies)
        return fight.StartFight()        

    def RoomIntroduction(self):
        return f"Tu arrive en face de {self._nbEnemies} ennemis"
    
    def GetEnemiNb(self) :
        return self._nbEnemies

class DefiRoom(Room):
    def __init__(self, name):
        self._name = name
        super().__init__()
    
    def RoomIntroduction(self):
        return f"Super, un peu de repos, tu arrives dans la salle {self._name}"
    
    @abstractmethod
    def StartGame(self):
        pass
    
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
            return False
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
        

    def ShowMatrice(self):
        rep=""
        rep+="    1   2   3"
        for i in range(3):
            rep+=f"\n {chr(65+i)}  {self.matrice[i][0]} | {self.matrice[i][1]} | {self.matrice[i][2]} \n   -----------"
        print(rep[:-11])


    def StartGame(self):
        computeurWin=False
        playerWin=False
        while playerWin == False and computeurWin==False and self.IsComplete()==False:
            self.MancheComputeur()
            computeurWin=self.Win("o")
            if not computeurWin:
                self.MancheJoueur()
                playerWin=self.Win("x")
        if playerWin : 
            print("Fin de la partie, vous avez gagné un le Talisman Rapidité")
            return True
        else:
            print("Vous avez perdu, bonne chance pour la suite")
            return False

    def IsComplete(self):
        for i in range(3):
            for j in range(3):
                if self.matrice[i][j]==" ":
                    return False
        return True     

    def MancheComputeur(self):
        self.ModifierMatrice(self.ComputerTour(),"o")
        self.ShowMatrice()
    
    def MancheJoueur(self,):
        self.ModifierMatrice(self.AskChoice(),"x")
        self.ShowMatrice()
    
    def Verif(self,rep):
        match rep :
            case "A1" : return self.matrice[0][0]==" "
            case "A2" : return self.matrice[0][1]==" "
            case "A3" : return self.matrice[0][2]==" "
            case "B1" : return self.matrice[1][0]==" "
            case "B2" : return self.matrice[1][1]==" "
            case "B3" : return self.matrice[1][2]==" "
            case "C1" : return self.matrice[2][0]==" "
            case "C2" : return self.matrice[2][1]==" "
            case "C3" : return self.matrice[2][2]==" "
            case _ : return False

    def AskChoice(self):
        rep = click.prompt("Quelle case souhaitez vous jouer?",type=CustomChoice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], case_sensitive=False), show_choices=False).upper()
        while not self.Verif(rep):
            print("Erreur la case est déjà utilisée")
            rep = click.prompt("Quelle case souhaitez vous jouer?",type=CustomChoice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"], case_sensitive=False), show_choices=False).upper()
        return rep

    def ModifierMatrice(self, choice,x):
        match choice :
            case "A1" : self.matrice[0][0]=x
            case "A2" : self.matrice[0][1]=x
            case "A3" : self.matrice[0][2]=x
            case "B1" : self.matrice[1][0]=x
            case "B2" : self.matrice[1][1]=x
            case "B3" : self.matrice[1][2]=x
            case "C1" : self.matrice[2][0]=x
            case "C2" : self.matrice[2][1]=x
            case "C3" : self.matrice[2][2]=x
            case _ : print("ERREUR")
    
    def ComputerTour(self):
        rep="-1"
        while self.Verif(rep)==False:
            rep=random.choice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])
        return rep
        
    def Win(self,x):
        if self.matrice[0][0]==x and self.matrice[0][1]==x and self.matrice[0][2]==x:
            return True
        if self.matrice[1][0]==x and self.matrice[1][1]==x and self.matrice[1][2]==x:
            return True
        if self.matrice[2][0]==x and self.matrice[2][1]==x and self.matrice[2][2]==x:
            return True
        if self.matrice[0][1]==x and self.matrice[1][1]==x and self.matrice[2][1]==x:
            return True
        if self.matrice[0][0]==x and self.matrice[1][0]==x and self.matrice[2][0]==x:
            return True
        if self.matrice[0][2]==x and self.matrice[1][2]==x and self.matrice[2][2]==x:
            return True
        if self.matrice[0][0]==x and self.matrice[1][1]==x and self.matrice[2][2]==x:
            return True
        if self.matrice[2][0]==x and self.matrice[1][1]==x and self.matrice[0][2]==x:
            return True
        return False
class Sphinx(DefiRoom):
    def __init__(self):
        super().__init__("Sphinx")
        self.liste = [("Quel est le langage informatique le plus utilisé chez les lycéens?","Python"),
                      ("Quels sont les 3 mots préférés de Monsieur Torinesi ?", "Vue de l'esprit"), 
                      ("Quelle est la marque d'ordinateur en 2 lettres?","hp")]
        self.questionChoisie=random.choice(self.liste)

    def RoomIntroduction(self):
        return r""" SPHINX
"""

    def AskQuestion(self):
        print(f"Pourras tu répondre à ma question :\n{self.questionChoisie[0]}")
    
    def GetAnswer(self):
        reponse=click.prompt("Quelle est ta réponse ?", type=str)
        return reponse

    def Verification(self, reponse):
        if self.liste==[]:
            print("Jeu fini")
        return CompareWord(reponse,self.questionChoisie[1])
    
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
            print("Vous n'avez rien gagné")
class Integrale(DefiRoom):
    def __init__(self):
        super().__init__("Intégrales")

    def StartGame(self):
        reponse=self.AskQuestion()
        if CompareWord(reponse, "ln2") :
            print("Bravo! Vous avez gagné le Talisman Puissance Calculatoire")
            return True
        else :
            print("Très mauvais calcul, bon courage pour la suite.")
            return False
        
    def AskQuestion(self)->str:
        
        print("Quelle est le résultat de l'integrale qui va s'afficher ?")
        
        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(5, 2))
        ax.axis("off")  # Hide axes
        # Render LaTeX formula
        ax.text(0.5, 0.5, r"$\int_{0}^{\infty} \frac{1}{e^x + 1} \,dx$", fontsize=20, ha="center")
        plt.show()
        
        return click.prompt("Resultat: ", type=str)


if __name__ == "__main__":
    #morpion = Morpion()
    #codeName = DefiRoom("codeName")
    #sphinx = DefiRoom("sphinx")
    #integrale = DefiRoom("intégrale")
    
    #code=CodeName()
    #print(code.RoomIntroduction())
    #code.StartGame()
    #morpion.StartGame()

    #shop=Shop("Shop")
    #print(shop.PaintRoom())

    Integrale().StartGame()
