from abc import ABC, abstractmethod
import click 
import questionary
import random
from Utils import * 
from sympy import integrate, symbols, oo, exp, ln, pprint, init_printing, latex, Integral
import matplotlib.pyplot as plt
from Player import *
from Combat import Fight
from Object import *
from time import sleep
from colorama import Fore


class Room(ABC):
    def __init__(self):
        self._voisin = {}

    @abstractmethod
    def RoomIntroduction(self):
        pass

    def GetVoisins(self):
        return self._voisin
    
    def GetEnemiNb(self):
        return 0
    
    def SetVoisins(self, nord=None, sud=None, est=None, ouest=None, passage=None):
        self._voisin["Nord"] = nord
        self._voisin["Sud"] = sud
        self._voisin["Est"] = est
        self._voisin["Ouest"] = ouest
        self._voisin["Passage"] = passage

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
        return f"Bienvenue au {self._name} ! \n"
    
    def PaintRoom(self):
        return Fore.BLUE + r"""
  __  __ ______ _   _ _    _ 
 |  \/  |  ____| \ | | |  | |
 | \  / | |__  |  \| | |  | |
 | |\/| |  __| | . ` | |  | |
 | |  | | |____| |\  | |__| |
 |_|  |_|______|_| \_|\____/ 
                                                         
""" + Fore.RESET
    
class Conseil(Room):
    def __init__(self):
        super().__init__()
    
    def RoomIntroduction(self):
        return "Tu veux un bon conseil ? Bah non."
    
    def StartConseil(self, playerLevel):
        Clear()
        NicePrint("Cest la fin de l'année.", 40)
        sleep(.75)
        NicePrint("\nTout le monde est content d'arriver au bout\n", 50)
        sleep(1)
        if playerLevel < 10:
            NicePrint("Seulement, tous n'en sortirons pas vainqueurs...", 50)
            sleep(.5)
            NicePrint("Et oui, tu n'as pas la moyenne, bon courage pour la suite !\n")

        else:
            NicePrint(f"Et tu t'en sors avec {playerLevel} points !")
            sleep(.5)
            NicePrint(f"Bravo ! Tu réussis l'année avec brio, mais je pense\nqu'un retour dans le passé ne te feras pas de mal..")
            sleep(.5)
            NicePrint(f"Le conseil a jugé que tu as de quoi etre encore meilleur, et te fais redoubler.")

        
        sleep(.75)
        print(f"{Fore.RED}Tu es mort...{Fore.RESET}")
        return playerLevel >= 10
    
class Shop(Room):
    def __init__(self, name):
        super().__init__()
        self._name=name
        self._objects=[("Gomme", 5),("Bouteille d'eau", 8)]
        self.antiseche = Antiseche("Antisèche",5)
        self.bouteille = Bouteille("Bouteille",10)
        self.montre = Montre("Montre",1)
        self.ameliorationTrousse = AmeliorationSac("Amélioration de la trousse",1)
        self.blanco = Blanco("Blanco",1)
        self.chatGPT = ChatGPT("ChatGPT",10,5)


        self.dicoAffichage={f'{self.antiseche.GetName()} : {5}€':(self.antiseche,5),
                            f'{self.bouteille.GetName()} : {10}€':(self.bouteille,10),
                            f'{self.montre.GetName()} : {100}€':(self.montre,100),
                            f'{self.blanco.GetName()} : {5}€': (self.blanco,5),
                            f'{self.chatGPT.GetName()} : {30}€': (self.chatGPT,30),
                            f'{self.ameliorationTrousse.GetName()} : {50}€':(self.ameliorationTrousse, 50),
                            f'Sortir du Shop': 0}
       
        #self.listeAffichageNomObjetsPrix=self.dicoAffichage.key()

    def RoomIntroduction(self):
        return f"Bienvenue au {self._name} ! \n"
    
    def ShowObjects(self):
        print(f"Voici les objets de la boutique : {self._objects}")
    
    def PaintRoom(self):
        return Fore.BLUE + r"""
########################################################################
#                ______   __                                           #
#                /      \ /  |                                         #
#               /$$$$$$  |$$ |____    ______    ______                 #
#               $$ \__$$/ $$      \  /      \  /      \                #
#               $$      \ $$$$$$$  |/$$$$$$  |/$$$$$$  |               #
#                $$$$$$  |$$ |  $$ |$$ |  $$ |$$ |  $$ |               #
#               /  \__$$ |$$ |  $$ |$$ \__$$ |$$ |__$$ |               #
#               $$    $$/ $$ |  $$ |$$    $$/ $$    $$/                #
#                $$$$$$/  $$/   $$/  $$$$$$/  $$$$$$$/                 #
#                                             $$ |                     #
#                                             $$ |                     #
#                                             $$/                      #
########################################################################
""" + Fore.RESET

    def AchatObjet(self, player:Player):
        prix=float("inf")
        print(f'Vous avez de {player.GetMoney()}€ dans votre portefeuille \n')
        sleep(1)
        while prix > player.GetMoney():
            rep = questionary.select("Quel objet voulez vous acheter?",choices=self.dicoAffichage.keys()).ask()
            if rep == "Sortir du Shop" : 
                return False
            if rep == "Amélioration de la trousse":
                return "Trousse"
            if player.AddItem(self.dicoAffichage[rep][0])==False:
                print("Vous n'avez pas assez de place dans votre inventaire, tentez d'améliorer la trousse?\n")
                return
            prix = self.dicoAffichage[rep][1]
            if prix > player.GetMoney(): # n'afficher que si le joueur est pauvre
                print("Vous n'avez pas assez d'argent, essayez peut-être un autre objet ?\n")
                return
            sleep(.5)
        player.ChangeMoney(-prix)
        print("Objet ajouté à l'inventaire, vous pourrez désormais l'utiliser en combat\n")
        sleep(1)
        return self.dicoAffichage[rep][0]
    

class FightRoom(Room):
    def __init__(self, ennemies:list[Enemi]):
        self._enemies = ennemies
        self._nbEnemies = len(ennemies)
        super().__init__()

    def StartFight(self, player):
        fight = Fight(player, self._enemies)
        return fight.StartFight()        

    def RoomIntroduction(self):
        if self.GetEnemiNb()==0:
            return "Cette salle est bien tranquille..."
        return f"\nTu arrive en face de {self.GetEnemiNb()} ennemis."
    
    def GetEnemiNb(self) :
        return len(self._enemies)

class DefiRoom(Room):
    def __init__(self, name):
        self._name = name
        super().__init__()
    
    def RoomIntroduction(self):
        return f"Super, un peu de repos, tu arrives dans la salle {self._name}"
    
    @abstractmethod
    def StartGame(self):
        pass

    def GetTalisman(self):
        return self.talismanType
    
class CodeName(DefiRoom):
    def __init__(self):
        super().__init__("Code Name")
        self.liste = [("police",("girophare","enfermer")),("barcelo",("cheveux","mathématiques"))]
        self.tupleJeu=random.choice(self.liste)
        self.talismanType = TalismanType.CodeName
        self.utilite="Tu peux désormais voir les prochains coups de l'adversaire!"

    def RoomIntroduction(self):
        return Fore.MAGENTA + r"""
 __   __   __   ___                     ___ 
/  ` /  \ |  \ |__     |\ |  /\   |\/| |__  
\__, \__/ |__/ |___    | \| /~~\  |  | |___ 
                                                                                                             
""" + Fore.RESET

    def AskQuestion(self):
        print(f"Je te donne 2 mots : {self.tupleJeu[1][0]} et {self.tupleJeu[1][1]}")
    
    def GetAnswer(self):
        reponse=click.prompt("A quoi je pense?", type=str)
        return reponse
            
    def GetUtilite(self):
        return self.utilite

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
        if self.StartManche()==True :
            return True
        else:
            print("Erreur, c'est votre dernière chance")
            if self.StartManche()==True:
                return True
            else : 
                print("Vous n'avez rien gagné")
                return False
            

class Morpion(DefiRoom):
    def __init__(self):
        super().__init__("Morpion")
        self.matrice=[[" "," "," ",],[" "," "," "],[" "," "," "]]
        self.talismanType = TalismanType.Morpion
        self.utilite="Une fois par combat tu pourras l'utiliser pour attaquer 2 fois d'affilée !"

    def RoomIntroduction(self):
        return Fore.MAGENTA + r"""
       __   __   __     __       
 |\/| /  \ |__) |__) | /  \ |\ | 
 |  | \__/ |  \ |    | \__/ | \| 
                                 
""" + Fore.RESET
    
            
    def GetUtilite(self):
        return self.utilite

    def ShowMatrice(self):
        rep=""
        rep+="    1   2   3"
        for i in range(3):
            rep+=f"\n {chr(65+i)}  {self.matrice[i][0]} | {self.matrice[i][1]} | {self.matrice[i][2]} \n   -----------"
        print(rep[:-11])


    def StartGame(self):
        Clear()
        computeurWin=False
        playerWin=False
        while playerWin == False and computeurWin==False and self.IsComplete()==False:
            Clear()
            self.ShowMatrice()
            sleep(.5)
            self.MancheComputeur() 
            Clear()           
            self.ShowMatrice()
            computeurWin=self.Win("o")
            if not computeurWin:
                self.MancheJoueur()
                playerWin=self.Win("x")
        self.ShowMatrice()
        return playerWin
    
            
    def GetUtilite(self):
        return self.utilite

    def IsComplete(self):
        for i in range(3):
            for j in range(3):
                if self.matrice[i][j]==" ":
                    return False
        return True     

    def MancheComputeur(self):
        self.ModifierMatrice(self.ComputerTour(),"o")
    
    def MancheJoueur(self,):
        self.ModifierMatrice(self.AskChoice(),"x")
    
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
        self.talismanType = TalismanType.Sphinx
        self.utilite="Tu pourras utiliser cette potion de guérison une fois par partie pour booster tes points de vie au maximum!"

        
    def GetUtilite(self):
        return self.utilite
    
    def RoomIntroduction(self):
        return Fore.MAGENTA+ r""" SPHINX
 __   __                  
/__` |__) |__| | |\ | \_/ 
.__/ |    |  | | | \| / \ 
                          
""" + Fore.RESET

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
            print("Bravo, vous avez gagné le Talisman Connaissance Ultime, " \
            "il te permet d'obtenir une potion de guérison à chaque partie")
            return True
        else:
            print("Vous n'avez rien gagné")
            return False
            
class Integrale(DefiRoom):
    def __init__(self):
        super().__init__("Intégrales")

        self.talismanType = TalismanType.Integrale
        self.utilite="Cette puissance calculatoire te permet, une fois par partie, de tuer un ennemi en 1 seul coup"

    def RoomIntroduction(self):
        return Fore.MAGENTA + r"""
       ___  ___  __   __             ___ 
| |\ |  |  |__  / _` |__)  /\  |    |__  
| | \|  |  |___ \__> |  \ /~~\ |___ |___ 
                                         
""" + Fore.RESET

    def StartGame(self):
        reponse=self.AskQuestion()
        if CompareWord(reponse, "ln2") :
            print("Bravo! Vous avez gagné le Talisman Puissance Calculatoire, il vous permettra de tuer un ennemi en un seul coup!")
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

    #Integrale().StartGame()
    #shop=Shop("shop")
    #codeName=CodeName()
    #codeName.StartGame()
    Conseil().StartConseil(15)