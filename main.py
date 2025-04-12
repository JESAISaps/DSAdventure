from Player import Player
import click
from Utils import *
from Room import DefiRoom, Sphinx, CodeName,Integrale, Morpion, FightRoom, Menu, Shop, Room
import questionary
import keyboard
import Map
from Object import *
from time import sleep

player = Player("Marine", 0)
fefe = Antiseche("Antisèche", 50)
menu=Map.menu
petit=Map.petitStart
shop=Map.shop
trioInfernal=Map.trioInfernalRoom
trioInfernalVide=Map.trioInfernalRoomVide


def LancerJeu():
    Starting()
    AttaqueTrioInfernal()

    while True:
        Map.initMap()
        player.Revive()
        Partie()


def Starting() -> bool :
    """
    Retourne True dès que les achats sont terminés
    """
    AffichageMenu()
    print("Appuyez sur Espace pour commencer le jeu \n")
    keyboard.wait("Space")
    AffichageShop()   

def AttaqueTrioInfernal(): 
    print(trioInfernal.RoomIntroduction())
    sleep(0.5)
    trioInfernal.StartFight(player)
    print("Tu es mort\n")

def Partie() -> bool :
    print("Appuyez sur Espace pour continuer le jeu \n")
    keyboard.wait("Space")
    AffichageShop()
    salleActuelle=trioInfernalVide
    sleep(0.5)
    while player.IsAlive():
        if isinstance(salleActuelle, FightRoom):
            AffichageRoomIntroduction(salleActuelle)
            sleep(0.5)
            if salleActuelle.StartFight(player)==False:
                print("Tu es mort \n")
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
    rep=questionary.select("Ou voulez vous aller?",choices=accessiblechoices).ask()
    return choices[rep]

def ActionShop():
    rep=questionary.select("Voulez vous acheter un objet?",choices=["Oui","Non, jouer"]).ask()
    #TODO AFFICHER LARGENT
    if rep=="Oui":
        objet=shop.AchatObjet(player)
        if objet != False :
            AjouterObjetInventaire(objet)
        else :
            print("C'est parti ! \n")
            sleep(1)
            return False
        return True
    else :
        print("C'est parti!\n")
        sleep(0.5)
        return False
    
def AjouterObjetInventaire(objet):
    player.GetBag().AddItem(objet)


def AffichageRoomIntroduction(salleActuelle):
    if salleActuelle.GetEnemiNb()==0:
        print("Les ennemis sont partis, tu peux avancer dans le labyrinthe \n")
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
