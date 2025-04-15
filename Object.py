from abc import ABC, abstractmethod
from Utils import ObjectType, Effect

class Object(ABC):
    def __init__(self, name):
        self._name = name
        self.objectType = ObjectType.Objet

    @property
    @abstractmethod
    def _description(self):
        pass

    def GetDescription(self):
        return self._description
    
    def GetName(self):
        return self._name

class Talisman(Object):
    def __init__(self, name):
        super().__init__(name)
        self._name = name
        self.objectType = ObjectType.Talisman

    @property
    def _description(self):
        return "Un talisman, il peut etre actif ou passif."
    
class UsableObject(Object):
    def __init__(self, name):
        super().__init__(name)
        self.objectType = ObjectType.Usable
        self._effect = Effect.AugmentationDegatPoint # Par defaut un item ajoute des degats.
        self.puissance = 1


    def Utiliser(self):
        return self._effect, self.puissance

    @property
    def _description(self):
        return "Un object utilisable."
    
    def GetPower(self):
        return self.puissance
    
    def GetEffectAsString(self):
        return "Rien"
    
    def GetEffectType(self) -> Effect:
        return self._effect

class Antiseche(UsableObject):
    def __init__(self, name, bonusDegat):
        super().__init__(name)
        self._effect = Effect.AugmentationDegatPoint
        self.puissance = bonusDegat

    @property
    def _description(self):
        return f"Rajoute {self.puissance} points de degats a la prochaine attaque"
    
    def GetEffectAsString(self):
        return f"+ {self.puissance} degats"

class Blanco(UsableObject):
    def __init__(self, name, nbAttaques):
        super().__init__(name)
        self._effect = Effect.AnnulationAttaque
        self.puissance = nbAttaques

    @property
    def _description(self):
        return "Annule la prochaine attaque de l'adversaire."
    
    def GetEffectAsString(self):
        return f"Annule {self.puissance} attaques de l'adversaire."
    
class AmeliorationSac(UsableObject):
    def __init__(self, name, puissance):
        super().__init__(name)
        self._effect = Effect.AmeliorationSac
        self.puissance = puissance

    @property

    def _description(self):
        return "Rajoute une place pour un objet dans la trousse"
    
    def GetEffectAsString(self):
        return f"+ {self.puissance} place d'inventaire"
    
""" TODO : Transformer en talisman
class Lunettes(UsableObject):
    def __init__(self):
        super().__init__()
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Permet de voir plus loin que les murs, mais attention tres fragile."
"""

class Montre(UsableObject):
    def __init__(self, name, efficacite:int):
        """
        """
        super().__init__(name)
        self._effect = Effect.AugmentationEsquive
        self.puissance = efficacite

    @property
    def _description(self):
        return "Permet d'esquiver la prochaine attaque."
    
    def GetEffectAsString(self):
        return f"+ {self.puissance} % d'esquiver les attaques"

class ChatGPT(UsableObject):
    def __init__(self, name, augAtkSelf, augAtkAdv):
        super().__init__(name)
        self._effect = Effect.AugmentationDegatReciproque
        self._augAtkAdv = augAtkAdv
        self._augAtkSelf = augAtkSelf
    
    def Utiliser(self):
        return self._effect, (self._augAtkSelf, self._augAtkAdv)

    @property
    def _description(self):
        return f"Augmente votre attaque de {self._augAtkSelf} mais augmente aussi l'attauque de l'adversaire de {self._augAtkAdv}."
    
    def GetEffectAsString(self):
        return f"+ {self._augAtkSelf} degats, mais aussi + {self._augAtkAdv} degats pur l'adversaire"

class Bouteille(UsableObject):
    def __init__(self, name, puissance):
        """
        0<puissance<100
        """
        super().__init__(name)
        self._effect = Effect.AugmentationPrecision
        self.puissance = puissance

    @property
    def _description(self):
        return "Augmente la precision."
    
    def GetEffectAsString(self):
        return f"+ {self.puissance} % de precision"
    
class PotionGuerison(UsableObject):
    def __init__(self, name):
        super().__init__(name)
        self._effect = Effect.PotGue
        self.puissance = -1
    
    @property
    def _description(self):
        return "Talisman créé pout te soigner."
    
    def GetEffectAsString(self):
        return f"Te soigne"


class EquipableObject(Object):
    def __init__(self, name, objectType:ObjectType, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__(name)
        self._defense=defense
        self._degat=degat
        self._pv=pv
        self._boostXp = boostXp
        self.objectType = objectType

    def GetDefense(self) -> int:
        return self._defense
    
    def GetDegat(self) -> int:
        return self._degat
    
    def GetPv(self) -> int:
        return self._pv
    
    def GetBoostXP(self) -> int:
        return self._boostXp
    
    
    @property
    def _description(self):
        return "Un object equipable."

class Armure(EquipableObject):
    def __init__(self, name, objectType:ObjectType=ObjectType.Objet, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__(name, objectType, defense, degat, pv, boostXp)

class Arme(EquipableObject):
    def __init__(self, name, objectType:ObjectType=ObjectType.Objet, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__(name, objectType, defense, degat, pv, boostXp)

if __name__ == "__main__":
    """stylo = Arme("Stylo style", defense = 0, degat = 10, pv=0)
    ordinateurGabin = Arme("Ordi-Nateur", defense=10, degat=20, pv=10)
    tong = Armure("tong-tong-tong-tong", defense=5, degat=0, pv=10)
    tshirt = Armure("tshirt tache", defense=10, degat=0, pv=10)
    fluo = Arme("fluo sec", defense=0, degat=15, pv=10)
    
    antiseche=Antiseche("Mouille", 10)
    
    print(antiseche.GetDescription())"""