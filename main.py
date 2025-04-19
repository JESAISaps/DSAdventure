"""
Script principal
"""
from Player import Player
from Utils import Clear, SkipLines, WaitForSpace, ViderInputBuffer, QUESTIONARYSTYLE, TalismanType, hide_cursor, show_cursor
from Room import FightRoom, Room, Conseil
import questionary
from Map import Map
from time import sleep
from colorama import Fore
from SaveGame import LoadGame, SaveGame

def LancerJeu():
    hide_cursor()
    Clear()
    carte = Map()
    menu=carte.menu
    trioInfernal=carte.trioInfernalRoom

    Starting(menu)
    if isFirstTime:
        AttaqueTrioInfernal(trioInfernal)
        SkipLines(3)
        WaitForSpace()

    GameLoop()
    

def GameLoop():
    """
    Starts Game Loop, it's an infinite loop.
    """
    while True:
        Clear()
        carte = Map()
        player.Revive()
        SaveGame(player)
        Partie(carte)
        print(Fore.RED + "Tu es mort." + Fore.RESET + "\n")
        WaitForSpace()


def Starting(menu) -> bool :
    """
    Retourne True dès que les achats sont terminés <- Faux
    """
    AffichageMenu(menu)
    WaitForSpace(True)

def AttaqueTrioInfernal(trioInfernalRoom:FightRoom):
    print("L'année commence déjà ! Tu arrives face à des professeurs redoutables, essaie de t'en sortir...")
    sleep(1.5)
    print(trioInfernalRoom.RoomIntroduction())
    sleep(0.5)
    trioInfernalRoom.StartFight(player)
    print(Fore.RED + "Tu es mort." + Fore.RESET)
    if player.GetLevel() == 0:
        print("\nBon tu fais un peu pitié, voici de quoi level up")
        player.AjouterXp(10)
        sleep(1)

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
                return
        else :
            show_cursor()
            if salleActuelle.StartGame() == True:
                player.RecompenseDefi(salleActuelle.GetTalisman(), salleActuelle.GetUtilite())
                
            else :
                print("Vous avez perdu, bonne chance pour la suite")
            hide_cursor()
        salleActuelle=ApresCombat(salleActuelle)

        if isinstance(salleActuelle, Conseil):
            salleActuelle.StartConseil(player.GetLevel())
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
    ViderInputBuffer()
    rep=questionary.select("Ou voulez vous aller?",choices=accessiblechoices, style=QUESTIONARYSTYLE).ask()
    if rep == "Equipement":
        EquiperJoueur()
        return False
    return choices[rep]

def EquiperJoueur():
    choix = {item.GetName():item for item in player.GetEquipableItems()}
    choix["Annuler"] = "Annuler"
    ViderInputBuffer()
    print("\nVotre équipement:")
    print(player.GetEquipementAffichage())
    reponse=questionary.select("Choisissez votre équipement", choices=choix.keys(), style=QUESTIONARYSTYLE).ask()
    if reponse != "Annuler" :
        player.EquipItem(choix[reponse])

def VerifLunettes():
    """
    Retourne True si le joueur possede les lunettes
    """
    return player.talismans[TalismanType.Morpion]

def ActionShop(shop):
    ViderInputBuffer()
    rep=questionary.select("Voulez vous acheter un objet?",choices=["Oui","Non, jouer"], style=QUESTIONARYSTYLE).ask()
    if rep=="Oui":
        objet=shop.AchatObjet(player)
        if objet == "Trousse":
            player.AmeliorerSac(1)
        return True
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

def AffichageMenu(menu:Room):
    print(menu.PaintRoom())
    print("\nBienvenue dans DSAdventure ! \n\n" \
    "Revis ton année de prépa en attaquant tes profs, gagne des Talismans, des objets et complète des minis jeux. \n" \
    "Ton objectif est d'arriver au conseil avec au moins 10 de moyenne!\n")

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
    isFirstTime = False
    player = LoadGame()
    if player == False:
        isFirstTime = True
        player = Player("Marine", 0, 3)
    LancerJeu()
