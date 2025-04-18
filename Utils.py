import click
from enum import Enum, auto
from dataclasses import dataclass
from colorama import Fore
import questionary
#from prompt_toolkit.styles import Style
import os
import keyboard
import msvcrt
from time import sleep
import sys
import os

if os.name == 'nt':
    import msvcrt
    import ctypes
    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

TIMETOWAITBETWEENATTACKS = .5

CHOICEYESORNO = [
    questionary.Choice(title=f'Oui'),
    questionary.Choice(title=f'Non')
]


QUESTIONARYSTYLE = questionary.Style([
    #('qmark', 'fg:#00ff00 bold'),     # Green question mark
    #('question', 'bold'),             # Bold question text
    #('answer', 'fg:#00ff00 bold'),    # Green answer when selected
    ('pointer', 'fg:#00ff00 bold'),   # Pointer › in green
    ('highlighted', 'bold')          # Highlighted item is bold
    #('selected', 'fg:#00ff00'),       # Selected item is green
])

    

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

def NicePrint(word, lettersBySeconds=60):
    """
    Prints the word letter by letter, with speed of letters by seconds
    """
    for letter in word:
        print(letter, end="", flush=True)
        sleep(1/lettersBySeconds)
    print()

def CompareWord(mot1 : str,mot2 : str) -> bool :
    mot1modifie=mot1.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    mot2modifie=mot2.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    return mot1modifie == mot2modifie

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class CustomChoice(click.Choice):
    def fail(self, value, param=None, ctx=None):
        raise click.BadParameter(
            f"Veuillez choisir parmi : {', '.join(self.choices)}"
        )
    
def WaitForSpace(isFirst=False):
    if (isFirst):
        print("Appuyez sur Espace pour" + Fore.CYAN + " commencer" + Fore.RESET +" le jeu \n")
    else:
        print("Appuyez sur Espace pour" + Fore.CYAN + " continuer" + Fore.RESET +" le jeu \n")
    hide_cursor()
    keyboard.wait("Space")

def SkipLines(nb):
    print("\n"*nb)
    
def ViderInputBuffer():
    while msvcrt.kbhit():
        msvcrt.getch()

class ObjectType(Enum):
    Objet = auto()
    Chapeau = auto()
    TShirt = auto()
    Chaussures = auto()
    Arme = auto()
    Talisman = auto()
    Usable = auto()
    Money = auto()

class TalismanType(Enum):
    CodeName = "Rapidité"
    Morpion = "Lunettes"
    Sphinx = "Connaissance ultime"
    Integrale = "Puissance calculatoire"
    def __str__(self):
        return str(self.value)


class Effect(Enum):
    AugmentationResistancePoint = "Augmentation de resitance"
    AugmentationDegatPoint = "Augmentation de degat"
    AugmentationResistancePourcentage = "Multiplication de resistance"
    AugmentationDegatPourcentage = "Multiplication de degat"
    AugmentationPrecision = "Augmentation de la precision"
    AnnulationAttaque = "Annulation de l'attaque"
    AugmentationEsquive = "Augmentation de l'esquive"
    AugmentationDegatReciproque = "Augmente les degats de tout le monde"
    AmeliorationSac = "Augmentation de la place dansla trousse"
    AugmentationDegatSelf = "Augmentation des dégats"
    AnnulationAttaqueSelf = "Tu t'endors"
    PotGue = "Tu re-gagne tous tes points de vie."

    def __str__(self):
        return str(self.value)

@dataclass(unsafe_hash=True)
class Money:
    amount:int
    objectType = ObjectType.Money

    def GetName(self):
        return f"Pieces - {self.amount}€"
    
    def GetAmount(self):
        return self.amount
    
    def __str__(self):
        return self.GetName()

class AttackStats(Enum):

    def __str__(self):
        return str(self.value)
    Degats = "Degats"

class LevelUpRewardType(Enum):
    BonusPv = auto()
    BonusAttaque = auto()
    BonusDefence = auto()
    BonusXp = auto()
    BonusVitesse = auto()
    BonusPrecision = auto()

if __name__ == "__main__":
    NicePrint("loikujyhtgvrcdexzdef'(ghynh gvfvrgthyjunh gvftghynhbgthyujnhbgvfc)", 60)
