from Player import *
import click
from Utils import *
from Room import DefiRoom, Sphinx, CodeName,Integrale, Morpion, FightRoom, Menu, Shop, Room
import questionary
import keyboard
from Map import Map
from Object import *
from time import sleep
from colorama import Fore

player = Player("Marine", 0)
fefe = Antiseche("Antisèche", 50)

def LancerJeu():
    Clear()
    carte = Map()
    menu=carte.menu
    shop=carte.shop
    trioInfernal=carte.trioInfernalRoom
    Starting(menu, shop)
    AttaqueTrioInfernal(trioInfernal)
    SkipLines(3)
    WaitForSpace()

    while True:
        Clear()
        carte = Map()
        player.Revive() 
        Partie(carte)


def Starting(menu, shop) -> bool :
    """
    Retourne True dès que les achats sont terminés <- Faux
    """
    AffichageMenu(menu)
    WaitForSpace(True)
    #AffichageShop(shop)

def AttaqueTrioInfernal(trioInfernalRoom:FightRoom): 
    print(trioInfernalRoom.RoomIntroduction())
    sleep(0.5)
    trioInfernalRoom.StartFight(player)
    print("Tu es mort\n")
    if player.GetLevel() == 0:
        print("\nBon tu fais un peu pitié, voici de quoi level up")
        player.AjouterXp(10)

def Partie(carte:Map) -> bool :
    AffichageShop(carte.shop)
    salleActuelle=carte.trioInfernalRoomVide
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
            if salleActuelle.StartGame() == True:
                player.AddTalisman(salleActuelle.GetTalisman())

        WaitForSpace()
        
        Clear()
        salleActuelle=AskWhereToGo(salleActuelle)
    WaitForSpace()
    
def AskWhereToGo(caseActuelle : Room)-> Room:
    choices=caseActuelle.GetVoisins()
    accessiblechoices=[]
    for i in choices.keys():
        if choices[i]!= None and i !="Passage":
            accessiblechoices.append(i)
        if i=="Passage" and VerifLunettes()==True :
            accessiblechoices.append(i)
    rep=questionary.select("Ou voulez vous aller?",choices=accessiblechoices).ask()
    return choices[rep]

def VerifLunettes():
    return player.talismans[1]==True

def ActionShop(shop):
    rep=questionary.select("Voulez vous acheter un objet?",choices=["Oui","Non, jouer"]).ask()
    if rep=="Oui":
        objet=shop.AchatObjet(player)
        if objet == "Trousse":
            player.AmeliorerSac(1)
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

def AffichageMenu(menu):
    print(menu.RoomIntroduction())
    print(menu.PaintRoom())

def AffichageShop(shop):
    """ 
    La fonction retourne True dès que le joueur veut commencer le jeu, sinon il est en train de faires des achats
    """    
    print(shop.PaintRoom())
    print(shop.RoomIntroduction())
    acheter=ActionShop(shop)
    while acheter != False:
        acheter=ActionShop(shop)
    return True


LancerJeu()