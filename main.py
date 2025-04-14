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
    # tests
    #caca = EquipableObject("iuytre", ObjectType.TShirt)
    #player.AddItem(caca)
    #EquiperJoueur()

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
    if player.GetLevel() == 0:
        print(Fore.RED + "Tu es mort." + Fore.RESET)
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
            if salleActuelle.StartGame() == True:
                player.AddTalisman(salleActuelle.GetTalisman())
        salleActuelle=ApresCombat(salleActuelle)
        WaitForSpace()
        Clear()
    WaitForSpace()

def ApresCombat(salleDepart):
    salleActuelle=AskWhereToGo(salleDepart)
    while salleActuelle == False:
        salleActuelle=AskWhereToGo(salleDepart)
    return salleActuelle
    
def AskWhereToGo(caseActuelle : Room)-> Room:
    choices=caseActuelle.GetVoisins()
    accessiblechoices=[]
    for i in choices.keys():
        if choices[i]!= None and i !="Passage":
            accessiblechoices.append(i)
        if choices[i]!= None and i=="Passage" and VerifLunettes()==True :
            accessiblechoices.append(i)
    if player.GetEquipableItems() != []:
        accessiblechoices.append("Equipement")
    flush_stdin()
    rep=questionary.select("Ou voulez vous aller?",choices=accessiblechoices).ask()
    if rep == "Equipement": 
        EquiperJoueur()
        return False
    return choices[rep]

def EquiperJoueur():
    choix = {item.GetName():item for item in player.GetEquipableItems()}
    choix["Annuler"] = "Annuler"
    print(choix)
    flush_stdin()
    reponse=questionary.select("Choisissez votre équipement", choices=choix.keys()).ask()
    if reponse != "Annuler" :
        player.EquipItem(choix[reponse])

def VerifLunettes():
    """
    Retourne True si le joueur possede les lunettes
    """
    return player.talismans[TalismanType.Morpion]

def ActionShop(shop):    
    flush_stdin()
    rep=questionary.select("Voulez vous acheter un objet?",choices=["Oui","Non, jouer"]).ask()
    if rep=="Oui":
        objet=shop.AchatObjet(player)
        if objet == "Trousse":
            player.AmeliorerSac(1)
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
    

if __name__ == "__main__":

    LancerJeu()
    