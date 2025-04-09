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




def Start():
    print(menu.RoomIntroduction())
    print(menu.PaintRoom())
    print("Appuyez sur Espace  pour commencer le jeu")
    keyboard.wait("Space")
    Game()


def Game():
    print(shop.PaintRoom())
    print(shop.RoomIntroduction())
    acheter=ActionShop()
    while acheter != False:
        acheter=ActionShop()
    SalleActuelle=shop
    while True:
        while player.IsAlive():
            SalleActuelle=AskWhereToGo(SalleActuelle)
            if type(SalleActuelle)==FightRoom:
                SalleActuelle.StartFight(player)
            else : 

                SalleActuelle.StartGame()
    

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
    else :
        return False

def AchatObjet():
    pass

Game()
