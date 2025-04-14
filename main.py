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

    while True:
        Clear()
        carte = Map()
        player.Revive() 
        Partie(carte)


def Starting(menu, shop) -> bool :
    """
    Retourne True dès que les achats sont terminés
    """
    AffichageMenu(menu)
    print("Appuyez sur Espace pour" + Fore.CYAN + " commencer" + Fore.RESET +" le jeu \n")
    keyboard.wait("Space")
    AffichageShop(shop)   

def AttaqueTrioInfernal(trioInfernalRoom:FightRoom): 
    print(trioInfernalRoom.RoomIntroduction())
    sleep(0.5)
    trioInfernalRoom.StartFight(player) 
    print("Tu es mort\n")

def WaitForSpace():
    print("Appuyez sur Espace pour continuer le jeu \n")
    keyboard.wait("Space")

def Partie(carte:Map) -> bool :
    WaitForSpace()
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
            if salleActuelle.StartGame() == True:
                player.AddTalisman(salleActuelle.GetTalisman())
        if player.GetEquipableItems() != []:
            EquiperJoueur()
        WaitForSpace()
        Clear()
        while salleActuelle != False : 
            salleActuelle=AskWhereToGo(salleActuelle)
    
def AskWhereToGo(caseActuelle : Room)-> Room:
    choices=caseActuelle.GetVoisins()
    accessiblechoices=[]
    for i in choices.keys():
        if choices[i]!= None and i !="Passage":
            accessiblechoices.append(i)
        if i=="Passage" and VerifLunettes()==True :
            accessiblechoices.append(i)
    if player.GetEquipableItems() != []:
        accessiblechoices.append("Equipement")
    rep=questionary.select("Ou voulez vous aller?",choices=accessiblechoices).ask()
    if rep == "Equipement": 
        EquiperJoueur()
        return False
    return choices[rep]

def EquiperJoueur():
    choices = player.GetEquipableItems().append("Annuler")
    reponse=questionary.select("Choisissez votre équipement", player.GetEquipableItems())
    if reponse != "Annuler" :
        player.EquipItem(reponse)
    else : pass

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