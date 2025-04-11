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
    AugmentationResistancePoint = auto()
    AugmentationDegatPoint = auto()
    AugmentationResistancePourcentage = auto()
    AugmentationDegatPourcentage = auto()
    AugmentationPrecision = auto()
    AnnulationAttaque = auto()
    AugmentationEsquive = auto()
    AugmentationDegatReciproque = auto()

@dataclass(unsafe_hash=True)
class Money:
    amount:int
    objectType = ObjectType.Money

    def GetName(self):
        return f"Pieces - {self.amount}€"

class AttackStats(Enum):
    Degats = "Degats"
    DelaiAttaque = "Recul Attaque"

class LevelUpRewardType(Enum):
    BonusPv = auto()
    BonusAttaque = auto()
    BonusDefence = auto()
    BonusXp = auto()
    BonusVitesse = auto()
    BonusPrecision = auto()