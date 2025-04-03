from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def _description(self):
        pass

    def GetDescription(self):
        return self._description

class Talisman(Object):
    def __init__(self, name):
        super().__init__()
        self._name = name

    @property
    def _description(self):
        return "Un talisman, il peut etre actif ou passif."
    
class UsableObject(Object):
    def __init__(self,):
        super().__init__()
    
    @abstractmethod
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Un object utilisable."

class Antiseche(UsableObject):
    def __init__(self, bonusDegat):
        super().__init__()
        self._bonusDegat = bonusDegat
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return f"Rajoute {self._bonusDegat} points de degats a la prochaine attaque"

class Blanco(UsableObject):
    def __init__(self):
        super().__init__()
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Annule la prochaine attaque de l'adversaire."

class Lunettes(UsableObject):
    def __init__(self):
        super().__init__()
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Permet de voir plus loin que les murs, mais attention tres fragile."

class Montre(UsableObject):
    def __init__(self):
        super().__init__()
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Permet d'augmenter les chances d'esquiver la prochaine attaque."

class ChatGPT(UsableObject):
    def __init__(self, augAtkSelf, augAtkAdv):
        super().__init__()
        self._augAtkAdv = augAtkAdv
        self._augAtkSelf = augAtkSelf
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return f"Augmente votre attaque de {self._augAtkSelf} mais augmente aussi l'attauque de l'adversaire de {self._augAtkAdv}."

class Bouteille(UsableObject):
    def __init__(self):
        super().__init__()
    
    def Utiliser():
        pass

    @property
    def _description(self):
        return "Augmente la precision."


class EquipableObject(Object):
    def __init__(self, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__()
        self._defense=defense
        self._degat=degat
        self._pv=pv
        self._boostXp = boostXp

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
    def __init__(self, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__(defense, degat, pv, boostXp)

class Arme(EquipableObject):
    def __init__(self, defense=0, degat=0, pv=0, boostXp=0):
        super().__init__(defense, degat, pv, boostXp)

if __name__ == "__main__":
    stylo = Arme(defense = 0, degat = 10, pv=0)
    ordinateurGabin = Arme(defense=10, degat=20, pv=10)
    tong = Armure(defense=5, degat=0, pv=10)
    tshirt = Armure(defense=10, degat=0, pv=10)
    fluo = Arme(defense=0, degat=15, pv=10)
    
    antiseche=Antiseche(10)
    
    print(antiseche.GetDescription())
    
    """blanco=Blanco()
    lunettes=Lunettes()
    montre=Montre()
    chatGPT=ChatGPT()
    bouteille=Bouteille()"""