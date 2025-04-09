from Player import Player, Enemi
#from Room import FightRoom
import questionary
from random import randint
from time import sleep
from Utils import TIMETOWAITBETWEENATTACKS

class Fight:
    def __init__(self, player:Player, enemiList:list[Enemi]):
        self._player:Player = player
        self._enemies:list[Enemi] = enemiList

        self._enemiNames = {enemi.GetName():enemi for enemi in enemiList}

    def StartFight(self):

        while self._enemies != [] and self._player.IsAlive(): #On continue tant qu'il y a des ennemis, et que le joueur est vivant.
            self.DoRound()

        if self._player.IsAlive():
            pass
            # TODO: Donner les recompenses, et terminer le combat.
        else:
            pass
            # TODO: Le joueur est mort, faut recommencer.

    def DoRound(self):
        self.PlayerTurn()
        self.EnemiTurn()

    def PlayerTurn(self):
        attackList = []
        enemiToAttack = self.GetEnemiToAttack()
        choice, damage = self.GetAttackPlayerChoice(attackList)
        #print(attackList)
        sleep(TIMETOWAITBETWEENATTACKS*2)
        print(f"Tu attaque {enemiToAttack.GetName()} pour {damage} degats avec {choice}")

    def EnemiTurn(self):
        if len(self._enemies) == 0:
            print("Plus d'ennemi")
            return
        enemiesToPLay:int = randint(0, len(self._enemies))

        for _ in range(enemiesToPLay+1):
            attackingEnemi = self._enemies[randint(0, len(self._enemies)-1)]
            attackName, damage = attackingEnemi.GetNextEnnemiAttack()
            sleep(TIMETOWAITBETWEENATTACKS)
            print(f"{attackingEnemi.GetName()} t'attaque avec {attackName} pour {damage} degats !")
            self._player.TakeDamage(damage)

    def GetAttackPlayerChoice(self, attackList):
        playerAttacks = self._player.GetAttacks()
        attacksToShow = ""
        for attack in playerAttacks:
            attacksToShow += attack + " :\n    "
            attackList.append(attack) # Pour les choix des questions
            for effect in playerAttacks[attack]:
                attacksToShow += f"{effect}: {playerAttacks[attack][effect]} || "
            attacksToShow = attacksToShow[:-3]
            attacksToShow += "\n"
        # Affiche la liste des attaques et leurs effects
        sleep(TIMETOWAITBETWEENATTACKS)
        print(attacksToShow)
        sleep(TIMETOWAITBETWEENATTACKS)
        choice = questionary.select("Quelle attaque voulez vous utiliser ?", choices=attackList, instruction=" ").ask()
        return choice, playerAttacks[choice]["Degats"]

    def GetEnemiToAttack(self):
        enemies = ""
        enemiNameList = []
        for enemi in self._enemies:
            enemiNameList.append(enemi.GetName())
            enemies += f" {enemi.GetName()} - {enemi.GetHp()} hp\n"
        
        print(enemies)
        choice = questionary.select("Quel ennemi voulez-vous attaquer ?", choices=enemiNameList).ask()
        return self._enemiNames[choice]
    
if __name__ == "__main__":
    player = Player("e")
    enemi = Enemi("r", 10)
    e2 = Enemi("ytrez", 10, [("cacatoutmou", 10)])

    fight = Fight(player, [enemi, e2])

    fight.StartFight()