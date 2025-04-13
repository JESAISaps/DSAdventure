import click
from enum import Enum, auto
from dataclasses import dataclass
from colorama import Fore
import questionary
from prompt_toolkit.styles import Style

TIMETOWAITBETWEENATTACKS = .5

CHOICEYESORNO = [
    questionary.Choice(title=f'Oui'),
    questionary.Choice(title=f'Non')
]


QUESTIONARYSTYLE = Style([
    #('qmark', 'fg:#00ff00 bold'),     # Green question mark
    #('question', 'bold'),             # Bold question text
    #('answer', 'fg:#00ff00 bold'),    # Green answer when selected
    ('pointer', 'fg:#00ff00 bold'),   # Pointer › in green
    ('highlighted', 'bold'),          # Highlighted item is bold
    #('selected', 'fg:#00ff00'),       # Selected item is green
])

def CompareWord(mot1 : str,mot2 : str) -> bool :
    mot1modifie=mot1.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    mot2modifie=mot2.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    return mot1modifie == mot2modifie

class CustomChoice(click.Choice):
    def fail(self, value, param=None, ctx=None):
        raise click.BadParameter(
            f"Veuillez choisir parmi : {', '.join(self.choices)}"
        )

class ObjectType(Enum):
    Objet = auto()
    Chapeau = auto()
    TShirt = auto()
    Chaussures = auto()
    Arme = auto()
    Talisman = auto()
    Usable = auto()
    Money = auto()

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
    DelaiAttaque = "Recul Attaque"

class LevelUpRewardType(Enum):
    BonusPv = auto()
    BonusAttaque = auto()
    BonusDefence = auto()
    BonusXp = auto()
    BonusVitesse = auto()
    BonusPrecision = auto()