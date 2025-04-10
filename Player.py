from abc import ABC, abstractmethod
import Object
from Utils import *

class Character(ABC):
    def __init__(self, name, startingHp):
        super().__init__()
        self._name = name
        self._hp = startingHp
        self._precision = 80
        self.evasion = 10
        self._resistance = 1
        self._isDead = False

        self._bonusPrecision = 0
        self._attackDelayEffect = 0
        self._bonusDamage = 0
        self._bonusResistance = 0
        self._bonusEvasion = 0

    @abstractmethod
    def Die(self):
        pass
    
    def TakeDamage(self, quantity):
        self._hp -= quantity*1/(self._bonusResistance+self._resistance)
        if self._hp <= 0:
            self.Die()

    def GetName(self):
        return self._name
    
    def GetHp(self):
        return self._hp
    
    def AddEffect(self, effet:Effect, power):
        #print(f"{effet} et la puissance {power}")
        match effet:
            case Effect.AnnulationAttaque:
                self._attackDelayEffect += power
            case Effect.AugmentationDegatPoint:
                self._bonusDamage += power
            case Effect.AugmentationDegatPourcentage:
                self._bonusDamage += 1+power/100
            case Effect.AugmentationResistancePoint:
                self._bonusResistance += power
            case Effect.AugmentationResistancePourcentage:
                self._bonusResistance *= 1+power/100
            case Effect.AugmentationPrecision:
                self._bonusPrecision += power
            case Effect.AugmentationEsquive:
                self._bonusEvasion += power

    def ActualizeEffectsAfterRound(self):
        if self._attackDelayEffect > 0:
            self._attackDelayEffect -= 1
        self._bonusDamage = 0
        self._bonusPrecision = 0
        self._bonusEvasion = 0
        self._bonusResistance = 0

    def GetAttackDelay(self):
        return self._attackDelayEffect
    
    def IsAlive(self):
        return not self._isDead
    

class Player(Character):

    class Sac:
        def __init__(self, startingSize:int):
            self.bagSize = startingSize
            self.content:list[Object.Object] = []

        def AddItem(self, item:Object.Object) -> bool:
            match item.objectType:
                case ObjectType.Talisman:
                    self.talismans[item] = True
                    return True
                case _: # On a un objet lambda
                    if len(self.content) >= self.bagSize:
                        return False # On ne peut pas inserer d'objet dans le sac
                    self.content.append(item)
                    return False
                
        def GetContent(self) -> list[Object.Object]:
            return self.content
        
        def RmItem(self, item):
            r"""
            /!\ Supprime l'existance de l'item specifié /!\ 
            """
            del item

        def Empty(self):
            return self.content == []

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

        self._attacks = {"Ecriture Soignee": {AttackStats.Degats:1}, "Boule de Fau":{AttackStats.Degats:1, "Etourdissement":5, "caca":"toujours"}}

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

    def GetAttacks(self) -> dict[str:dict[str:int]]:
        return self.GetDicoAttacksWithModifiedDamage()
    
    def GetDicoAttacksWithModifiedDamage(self):
        rep = {}
        for attaque in self._attacks:
            rep[attaque] = {}
            for stat in self._attacks[attaque]:
                if stat == AttackStats.Degats: # Si la stat est les degats, alors on augmente les degats selon le bonus
                    rep[attaque][stat] = self._attacks[attaque][stat] + self._bonusDamage
                else:
                    rep[attaque][stat] = self._attacks[attaque][stat]
        return rep
    def AddTalisman(self, id):
        self.talismans[id]=True

    def GetUsableObjects(self) -> list[Object.UsableObject]:
        rep = []
        for item in self.GetBag().GetContent():
            if item.objectType == ObjectType.Usable:
                rep.append(item)

        return rep
    
    

class Enemi(Character):
    def __init__(self, name, startingHp=5, attacks=[("Coup de poing",2), ("Coup de regle",1), ("Coup de tete",10)]):
        super().__init__(name, startingHp)
        self.dropPossibilities = []
        self._attacks = attacks
        self._firstAttack = attacks[0]

    def Die(self):
        self._isDead = True
        del self

    def GetNextEnnemiAttack(self)->tuple[str, int]:
        if len(self._attacks) == 0:
            return self._firstAttack
        return self._attacks.pop(0)

if __name__ == "__main__":
    player = Player("z", 10)    
    print(player._xp)
    print(player._level)
