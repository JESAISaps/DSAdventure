from abc import ABC, abstractmethod
import Object
from Utils import *
from random import randint
from colorama import Fore
from copy import copy

class Character(ABC):
    def __init__(self, name, startingHp, level=0, color=Fore.WHITE):
        super().__init__()
        self._name = name
        self._hp = startingHp
        self._maxHp = startingHp
        self._precision = 80
        self._evasion = 10
        self._resistance = 1
        self._isDead = False
        self._level = level

        self._bonusPrecision = 0
        self._attackDelayEffect = 0
        self._bonusDamage = 0
        self._bonusResistance = 0
        self._bonusEvasion = 0

        self._nameColor = color

        self.armorBonusDef = 0

    @abstractmethod
    def Die(self):
        pass
    
    def TakeDamage(self, quantity):
        self._hp -= quantity*1/(self._bonusResistance+self._resistance + self.armorBonusDef)
        if self._hp <= 0:
            self.Die()

    def GetName(self):
        return f"{self._name}"
    
    def GetHp(self):
        return self._hp
    
    def GetLevel(self):
        return self._level
    
    def GetPrecision(self):
        return self._precision
    
    def GetEvasion(self):
        return self._evasion
    
    def AddEffect(self, effet:Effect, power):
        #print(f"{effet} et la puissance {power}")
        print(f"{self.GetName()} recois l'effet {effet}")
        match effet:
            case Effect.AnnulationAttaque:
                self._attackDelayEffect += power
                #print(f"DEBUG Character.AddEffect: A ajouté effet annulAtt a {self.GetName()}")
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
            case Effect.AmeliorationSac:
                self.AmeliorerSac(power)
            case Effect.AugmentationDegatSelf:
                self._bonusDamage += power
            case _:
                print("Erreur Character.AddEffect effet non reconnu")

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
    
    def ReduceAttackDelayAfterTry(self):
        self._attackDelayEffect -= 1
    

class Player(Character):

    class Sac:
        def __init__(self, startingSize:int):
            self.bagSize = startingSize
            self.content:list[Object.Object] = []
            

        def AddItem(self, item:Object.Object) -> bool:
                if len(self.content) >= self.bagSize:
                    return False # On ne peut pas inserer d'objet dans le sac
                self.content.append(item)
                return True
        
        

                
        def GetContent(self) -> list[Object.Object]:
            return self.content
        
        def GetBagSize(self):
            return self.bagSize
        
        def GetEmptySpacesNb(self):
            return self.bagSize - len(self.content)
        
        def RmItem(self, item):
            r"""
            supprime l'item de l'inventaire d'un joueur.
            """
            self.content.remove(item)

        def isEmpty(self):
            return self.content == []

        def RemoveAllItems(self):
            self.content = []
    class Equipement:
        def __init__(self):
            self.equiped:dict[ObjectType:Object.EquipableObject] = {ObjectType.Arme:None, ObjectType.Chapeau:None,ObjectType.TShirt:None, ObjectType.Chaussures:None}
        
            self.bonusDef = 0
            self.bonusHp = 0
            self.bonusDamage = 0
            self.bonusXp = 0

        def EquipItem(self, item:Object.EquipableObject) -> Object.EquipableObject | None:            
            old = self.equiped[item.objectType]
            self.equiped[item.objectType] = item
            return old        
        
        def CalculerBonusEquipement(self):
            for objectType in self.equiped:
                if self.equiped[objectType] is not None:
                    self.bonusDamage += self.equiped[objectType].GetDegat()
                    self.bonusDef += self.equiped[objectType].GetDefense()
                    self.bonusHp += self.equiped[objectType].GetPv()
                    self.bonusXp += self.equiped[objectType].GetBoostXP()

        def GetEquiped(self):
            return copy(self.equiped)
        
        def GetDefense(self) -> int:
            return self.bonusDef
    
        def GetDegat(self) -> int:
            return self.bonusDamage

        def GetPv(self) -> int:
            return self.bonusHp

        def GetBoostXP(self) -> int:
            return self.bonusXp


    def __init__(self,name,xp=0, bagSize=2, startingHp=5):
        super().__init__(name, startingHp, color=Fore.CYAN) #Tous les joueurs commencent avec 10 PV au niveau 0

        self.sac = self.Sac(bagSize)
        self.equipement = self.Equipement()
        self._baseDamage = 0

        dicoTalisman = {TalismanType.CodeName:("CodeName","Rapidité"),TalismanType.Morpion:("Morpion","Lunettes"),TalismanType.Sphinx:("Sphinx","Connaissance ultime"),TalismanType.Integrale:("Integrale","Puissance calculatoire")}
        self.talismans = {id:False for id in dicoTalisman}

        self.armorBonusDef = 0
        self.armorBonusHp = 0
        self.armorBonusDamage = 0
        self.armorBonusXp = 0

        self._money = 0
        self._xp=0
        self._level = 0
        self._xpCap = [10, 50, 100, 200, 250, 300, 500, 750, 1000, 2000, 3250, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 50000, 100000]
        self.AjouterXp(xp)
        # Recompense de level up des stats de la forme {niveau:[bonusVie, bonusArmure, bonusDegat, bonusVitesse, bonusPrecision]}
        self._recompensesLevelUpStats = {1:[5, 1, 3, 1, 1],
                                         2:[2, 1, 1, 1, 1],
                                         3:[2, 1, 1, 1, 1],
                                         4:[1, 1, 5, 1, 1],
                                         5:[5, 1, 1, 1, 1],
                                         6:[7, 1, 3, 1, 1],
                                         7:[7, 1, 3, 1, 1],
                                         8:[7, 1, 3, 1, 1],
                                         9:[7, 1, 3, 1, 1],
                                         10:[5, 1, 3, 1, 1],
                                         11:[5, 1, 3, 1, 1],
                                         12:[5, 1, 3, 1, 1],
                                         13:[5, 1, 3, 1, 1],
                                         14:[5, 1, 3, 1, 1],
                                         15:[5, 1, 3, 1, 1],
                                         16:[5, 1, 3, 1, 1],
                                         17:[5, 1, 3, 1, 1],
                                         18:[5, 1, 3, 1, 1],
                                         19:[5, 1, 3, 1, 1],
                                         20:[5, 1, 3, 1, 1]}
        
        #TODO: mettre les recompenses de capacite
        temp = [("0 étoiles",{AttackStats.Degats:0, Effect.AnnulationAttaque:1}), #1
                (),
                ("Negligeation", {AttackStats.Degats:5, Effect.AugmentationDegatPourcentage:.2}),
                ("Révisions", {AttackStats.Degats:1, Effect.AugmentationDegatSelf:5, Effect.AugmentationPrecision:15}),
                ("Absence", {AttackStats.Degats:-1, Effect.AugmentationEsquive:60}),
                ("Revisions Nocturnes", {AttackStats.Degats:20, Effect.AnnulationAttaqueSelf:2}),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                (),
                ()
                ]
        self._recompenceCapaciteLevelUp = {i+1:temp[i] for i in range(0,20)}
        self._attacks = {"Ecriture Soignee": {AttackStats.Degats:1}}

    def GetMoney(self):
        return self._money
    
    def ChangeMoney(self,qte):
        self._money += qte

    def SetMoney(self,qte):
        self._money = qte

    def AjouterXp(self,quantite):
        quantite*= (1+self.equipement.GetBoostXP())
        while (self._xp+quantite)>=self._xpCap[self._level]:
            quantite -= self._xpCap[self._level] - self._xp
            self.LevelUp()

        self._xp += quantite

    def LevelUp(self):
        self._level+=1
        self._xp = 0
        self.AjouterLevelUpBonuses()
        print(f"Bravo tu as gagné un point de moyenne, tu es a present à {Fore.BLUE}{self.GetLevel()}/20{Fore.RESET} !")
    
    def AjouterLevelUpBonuses(self):
        level = self.GetLevel()
        self.LevelUpStats(self._recompensesLevelUpStats[level])
        self.AjouterCapa(self._recompenceCapaciteLevelUp[level])

    def AjouterCapa(self, capa):
        print(capa)
        if len(capa) != 0:
            self._attacks.update({capa[0]:capa[1]})

    def LevelUpStats(self, bonus:list):
        # bonus de la forme [bonusVie, bonusArmure, bonusDegat, bonusVitesse, bonusPrecision]
        self._maxHp += bonus[0]
        self._resistance += bonus[1]
        self._baseDamage += bonus[2]
        self._evasion += bonus[3]
        self._precision += bonus[4]

    def AmeliorerSac(self, power):
        self.sac.bagSize += power
        print(f"Tu as ajouté {power} places dans ta trousse !")

    def Die(self):
        self.sac.RemoveAllItems()
        self._isDead = True

    def GetXpCaps(self, level):
        return self._xpCap[level]

    def Revive(self):
        self._isDead = False
        self._hp = self._maxHp + self.armorBonusDamage

    def GetBag(self) -> Sac:
        return self.sac

    def GetAttacks(self) -> dict[str:dict[AttackStats.Degats:int]]:
        return self.GetDicoAttacksWithModifiedDamage()
    
    def GetDicoAttacksWithModifiedDamage(self):
        rep = {}
        for attaque in self._attacks:
            rep[attaque] = {}
            for stat in self._attacks[attaque]:
                if stat == AttackStats.Degats: # Si la stat est les degats, alors on augmente les degats selon le bonus
                    rep[attaque][stat] = (self._attacks[attaque][stat] + self.GetBaseDamage()) + self._bonusDamage
                else:
                    rep[attaque][stat] = self._attacks[attaque][stat]
        return rep
    
    def GetBaseDamage(self):
        return self._baseDamage + self.armorBonusDamage
    
    def GetBaseArmor(self):
        return self._resistance + self.armorBonusDef
    
    def AddTalisman(self, id):
        self.talismans[id]=True

    def GetUsableObjects(self) -> list[Object.UsableObject]:
        rep = []
        for item in self.GetBag().GetContent():
            if item.objectType == ObjectType.Usable:
                rep.append(item)

        return rep
    
    def AddItem(self, item:Object.Object | Money):
        #print(item.objectType)
        match item.objectType:
                case ObjectType.Talisman:
                    self.talismans[item] = True
                    return True
                case ObjectType.Money:
                    self._money += item.amount
                    return True
                case _: # On a un objet lambda
                    return self.sac.AddItem(item)
    
    def RemoveItem(self, item):
        self.sac.RmItem(item)

    def EquipItem(self, item):
        oldItem = self.equipement.EquipItem(item)
        self.RemoveItem(item)
        if oldItem is not None:
            self.AddItem(oldItem)

        self.equipement.CalculerBonusEquipement()
        self.ActualiezEquipmentBonuses()
    
    def ActualiezEquipmentBonuses(self):
        self.armorBonusDef = self.equipement.GetDefense()
        self.armorBonusDamage = self.equipement.GetDegat()
        self.armorBonusHp = self.equipement.GetPv()

    def GetEquipableItems(self):
        return [item for item in self.sac.content if item.objectType in [ObjectType.Arme, ObjectType.Chapeau, ObjectType.Chaussures, ObjectType.TShirt]]
    
    def PrintEquipment(self):
        equipedItems = self.equipement.GetEquiped()
        return f"Tete: {equipedItems[ObjectType.Chapeau]}\n\nCorp: {equipedItems[ObjectType.TShirt]}\
       Arme: {equipedItems[ObjectType.Arme]}\n\n Bas: {equipedItems[ObjectType.Chaussures]}"
        
    
    
class Enemi(Character):
    def __init__(self, name, startingHp=5, attacks=[("Coup de poing",2), ("Coup de regle",1), ("Coup de tete",10)], level = 0, esquive=10):
        super().__init__(name, startingHp, level=level)
        # Les proba sont nb/150
        self.dropPossibilities = {Money(amount=randint(2, (self.GetLevel()+2)*3)):130,
                                    
                                    Object.Armure("Casquette Stylée", objectType=ObjectType.Chapeau, defense=2, degat=0, pv=5): 4,
                                    Object.Armure("T-Shirt Déchiré", objectType=ObjectType.TShirt, defense=1, degat=0, pv=3): 5,
                                    Object.Armure("Bottes Cloutées", objectType=ObjectType.Chaussures, defense=4, degat=1, pv=6): 5,
                                    Object.Armure("Stylo de Bureau", objectType=ObjectType.Arme, defense=0, degat=8, pv=0): 4,
                                    Object.Armure("Pull de Mamie", objectType=ObjectType.TShirt, defense=3, degat=0, pv=8): 3,
                                    Object.Armure("Lunettes de Nerd", objectType=ObjectType.Chapeau, defense=1, degat=1, pv=2): 2,

                                    Object.Antiseche("Mouille", 10): 7,
                                    Object.Antiseche("Carton Plié", 7): 15,
                                    Object.Bouteille("Bouteille de Courage", 12): 10,
                                    Object.Blanco("Blanco Magique", 9): 6,
                                    Object.Montre("Montre Casse-Tête", 11): 5,
                                    Object.ChatGPT("ChatGPT", 15, 7): 5,
                                    Object.AmeliorationSac("Trousse ++", 2):25
                                    }
        self._attacks = copy(attacks)
        self._firstAttack = attacks[0]

        self._evasion = esquive

    def Die(self):
        self._isDead = True
        del self

    def GetNextEnnemiAttack(self)->tuple[str, int]:
        if len(self._attacks) == 0:
            return self._firstAttack
        return self._attacks.pop(0)
    
    def SetDropPossibilities(self, dropTable:dict[Object:int]):
        self.dropPossibilities = dropTable
    def AddDropPossibilitie(self, drop:Object.Object | Money, proba:int):
        self.dropPossibilities[drop] = proba

    def GetDropTable(self):
        return self.dropPossibilities

if __name__ == "__main__":
    player = Player("z", 10)    
    print(player._xp)
    print(player._level)
