import click
from enum import Enum, auto

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

class Effect(Enum):
    ResistancePoint = auto()
    AugmentationDegatPoint = auto()
    RestancePourcentage = auto()
    AugmentationDegatPourcentage = auto()
    AugmentationPrioriteCombat = auto()
    AugmentationPrecision = auto()
    AnnulationAttaque = auto()
    AugmentationEsquive = auto()
    AugmentationDegatReciproque = auto()