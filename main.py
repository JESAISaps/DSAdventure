from Player import Player
import click
from Utils import *
from Room import DefiRoom, Sphinx, CodeName,Integrale, Morpion, FightRoom, Menu, Shop, Room
import questionary
import keyboard
import Map

player = Player("Jean", 0)
menu=Map.menu
petit=Map.petitStart
shop=Map.shop
trioInfernal=Map.trioInfernalRoom
trioInfernalVide=Map.trioInfernalRoomVide


def LancerJeu():
    Starting()
    AttaqueTrioInfernal()

    while True:
        player.Revive()
        Partie()


def Starting() -> bool :
    """
    Retourne True dès que les achats sont terminés
    """
    AffichageMenu()
    print("Appuyez sur Espace pour commencer le jeu")
    keyboard.wait("Space")
    AffichageShop()   

def AttaqueTrioInfernal(): 
    print(trioInfernal.RoomIntroduction())
    trioInfernal.StartFight(player)
    print("Tu es mort")

def Partie() -> bool :
    print("Appuyez sur Espace pour continuer le jeu")
    keyboard.wait("Space")
    AffichageShop()
    salleActuelle=trioInfernalVide
    while player.IsAlive():
        if isinstance(salleActuelle, FightRoom):
            AffichageRoomIntroduction(salleActuelle)
            if salleActuelle.StartFight(player)==False:
                print("Tu es mort")
                return False
            else :
                pass
        else : 
            salleActuelle.StartGame() 
            #TODO RETURN BOOL ADD TALISMAN 
            
        salleActuelle=AskWhereToGo(salleActuelle)
    

def AskWhereToGo(caseActuelle : Room)-> Room:
    choices=caseActuelle.GetVoisins()
    accessiblechoices=[]
    for i in choices.keys():
        if choices[i]!= None:
            if i=="Passage":
                pass
                #TODO Verif si Lunettes
            else :
                accessiblechoices.append(i)
    rep=questionary.select("Ou voulez vous aller?",accessiblechoices).ask()
    return choices[rep]

def ActionShop():
    rep=questionary.select("Voulez vous acheter un objet?",choices=["Oui","Non, jouer"]).ask()
    #TODO AFFICHER LARGENT
    if rep=="Oui":
            AchatObjet()
            return True
    else :
        print("C'est parti!")
        return False
    

def AchatObjet():
    pass

def AffichageRoomIntroduction(salleActuelle):
    if salleActuelle.GetEnemiNb()==0:
        print("Les ennemis sont partis, tu peux avancer dans le labyrinthe, ou récupérer des objets s'il y en a")
    else :
        print(salleActuelle.RoomIntroduction())

def AffichageMenu():
    print(menu.RoomIntroduction())
    print(menu.PaintRoom())

def AffichageShop():
    """ 
    La fonction retourne True dès que le joueur veut commencer le jeu, sinon il est en train de faires des achats
    """    
    print(shop.PaintRoom())
    print(shop.RoomIntroduction())
    acheter=ActionShop()
    while acheter != False:
        acheter=ActionShop()
    return True


LancerJeu()
