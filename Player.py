from abc import ABC, abstractmethod
import Object
from Utils import *

class Character(ABC):
    def __init__(self, name, startingHp):
        super().__init__()
        self._name = name
        self._hp = startingHp

    @abstractmethod
    def Die(self):
        print("Le joueur est mort")
    
    def TakeDamage(self, quantity):
        self._hp -= quantity
        if self._hp <= 0:
            self.Die()

    def GetName(self):
        return self._name
    
    def GetHp(self):
        return self._hp

class Player(Character):

    class Sac:
        def __init__(self, startingSize:int):
            self.bagSize = startingSize
            self.content = []

        def AddItem(self, item:Object) -> bool:
            match item:
                case Object.Talisman:
                    self.talismans[item] = True
                    return True
                case _: # On a un objet lambda
                    if len(self.sac >= self.bagSize):
                        return False # On ne peut pas inserer d'objet dans le sac
                    self.sac.append(item)
                    return False
                
        def GetBagContent(self) -> list:
            return self.content
        
        def RmItem(self, item):
            """
            /!\ Supprime l'existance de l'item specifié
            """
            del item

    class Equipement:
        def __init__(self):
            self.equiped:dict[int:Object.EquipableObject] = {1:None, 2:None,3:None, 4:None}
        
        def EquipItem(self, item:Object.EquipableObject) -> Object.EquipableObject | None:            
            old = self.equiped[item.objectType.value]
            self.equiped[item.objectType.value] = item
            return old
        
        def GetBonusStats(self):
            bonusDef = 0
            bonusHp = 0
            bonusDamage = 0
            bonusXp = 0
            # TODO: donner les stats


    def __init__(self,name,xp=0, bagSize=2):
        super().__init__(name, 5) #Tous les joueurs commencent avec 5 PV au niveau 0

        self.sac = self.Sac(bagSize)


        dicoTalisman = {1:("CodeName","Lecture des pensées"),2:("Morpion","Rapidité"),3:("Sphinx","Connaissance ultime"),4:("Integrale","Puissance calculatoire")}
        self.talismans = {id:False for id in dicoTalisman}

        self._xp=0
        self._level = 0
        self._xpCap = [10, 50, 100, 200, 250, 300, 500, 750, 1000, 2000, 3250, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 50000, 100000]
        self.AjouterXp(xp)

        self._attacks = {"Ecriture Soignee": {"Degats":1}, "Boule de Fau":{"Degats":1, "Etourdissement":5, "caca":"toujours"}}

        self._isDead = False

    def AjouterXp(self,quantite):
        while (self._xp+quantite)>=self._xpCap[self._level]:
            quantite -= self._xpCap[self._level] - self._xp
            self.LevelUp()

        self._xp += quantite

    def LevelUp(self):
        self._level+=1
        self._xp = 0

    def Die(self):
        self.sac = []
        self._isDead = True

    def GetBag(self) -> Sac:
        return self.sac

    def IsAlive(self):
        return not self._isDead
    
    def GetAttacks(self):
        return self._attacks
    
    def AddTalisman(self, id):
        self.talismans[id]=True



class Enemi(Character):
    def __init__(self, name, startingHp=5, attacks=[("Coup de poing",2), ("Coup de regle",1), ("Coup de tete",10)]):
        super().__init__(name, startingHp)
        self.dropPossibilities = []
        self._attacks = attacks
        self._firstAttack = attacks[0]

    def Die():
        pass

    def GetNextEnnemiAttack(self)->tuple[str, int]:
        if len(self._attacks) == 0:
            return self._firstAttack
        return self._attacks.pop(0)

if __name__ == "__main__":
    player = Player("z", 10)    
    print(player._xp)
    print(player._level)