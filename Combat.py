from Player import Player, Enemi
from Room import FightRoom
import questionary

class Fight:
    def __init__(self, player:Player, enemiList:list[Enemi]):
        self._player:Player = player
        self._enemies:list[Enemi] = enemiList

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
        attackList = []
        choice = self.GetPlayerChoice(attackList)
        print(attackList)
        print(choice)
        

    def GetPlayerChoice(self, attackList):
        playerAttacks = self._player.GetAttacks()
        attacksToShow = ""
        for attack in playerAttacks:
            attacksToShow += attack + " :\n    "
            attackList.append(attack) # Pour les choix des questions
            for effect in playerAttacks[attack]:
                attacksToShow += f"{effect}: {playerAttacks[attack][effect]} || "
            attacksToShow = attacksToShow[:-3]
            attacksToShow += "\n"
        print(attacksToShow)
        return questionary.select("Quelle attaque voulez vous utiliser ?", choices=attackList, instruction=" ").ask()

if __name__ == "__main__":
    player = Player("e")
    enemi = Enemi("r", 10)

    fight = Fight(player, [enemi])

    fight.StartFight()