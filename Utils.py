import click
from enum import Enum, auto
from dataclasses import dataclass

TIMETOWAITBETWEENATTACKS = .5

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
    AugmentationDegatReciproque = auto()
    AmeliorationSac = auto()

    def __str__(self):
        return str(self.value)

@dataclass(unsafe_hash=True)
class Money:
    amount:int
    objectType = ObjectType.Money

    def GetName(self):
        return f"Pieces - {self.amount}€"
    
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