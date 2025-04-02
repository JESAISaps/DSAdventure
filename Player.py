from abc import ABC, abstractmethod
import Object

class Character(ABC):
    def __init__(self, name, startingHp):
        super().__init__()
        self._name = name
        self._hp = startingHp

    @abstractmethod
    def Die(self):
        pass
    
    def TakeDamage(self, quantity):
        self._hp -= quantity
        if self <= 0:
            self.Die()

class Player(Character):
    def __init__(self,name,xp=0, bagSize=2):
        super().__init__(name, 5) #Tous les joueurs commencent avec 5 PV au niveau 0

        self.sac = []
        self.bagSize = 4

        allTalismans = ["CodeName", "Morpion", "Sphinx", "Integrale"]
        self.talismans = {nom:False for nom in allTalismans}

        self._xp=0
        self._level = 0
        self._xpCap = [10, 50, 100, 200, 250, 300, 500, 750, 1000, 2000, 3250, 5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 50000, 100000]
        self.AjouterXp(xp)

        self._attacks = {"Ecriture Soignee": {"Degats":1}, "Boule de Fau":{"Degat":1, "Etourdissement":5}}

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

    def GetBag(self):
        return self.sac

    def IsAlive(self):
        return not self._isDead
    
    def GetAttacks(self):
        return self._attacks


class Enemi(Character):
    def __init__(self, name, startingHp):
        super().__init__(name, startingHp)
        self.dropPossibilities = []

    def Die():
        pass

if __name__ == "__main__":
    player = Player("z", 10)    
    print(player._xp)
    print(player._level)