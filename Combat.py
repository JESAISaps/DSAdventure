from Player import Player, Enemi
from Object import UsableObject, Object, Antiseche
#from Room import FightRoom
import questionary
import random
from time import sleep
from Utils import TIMETOWAITBETWEENATTACKS, Effect

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
            print("Bravo tu as gagne")
            # TODO: Donner les recompenses, et terminer le combat.
        else:
            pass
            print("nul tu as perdu")
            # TODO: Le joueur est mort, faut recommencer.

    def DoRound(self):
        self.PlayerTurn()
        self.EnemiTurn()

        self.EndRound()

    def EndRound(self):
        self._player.ActualizeEffectsAfterRound()
        for enemi in self._enemies:
            enemi.ActualizeEffectsAfterRound()

    def PlayerTurn(self):
        if self._player.GetAttackDelay() > 0:
            print("Tu ne peux pas attaquer.")
            return

        itemToUse:UsableObject = self.AskForObjectUse()
        if itemToUse != False:
            match itemToUse.GetEffectType(): # Utile si dans le futur on a + d'effets particuliers
                case Effect.AugmentationDegatReciproque: # Dans ce cas la on augmente l'ennemi et le joueur
                    effet = itemToUse.Utiliser()
                    random.choice(self._enemies).AddEffect(effet[0], effet[1][1])
                    self._player.AddEffect(effet[0], effet[1][0])
                case Effect.AnnulationAttaque:
                    enemiToApplyEffect = self.GetEnemiToAttack("Sur quel ennemi voulez vous appliquer l'effet ?")
                    enemiToApplyEffect.AddEffect(*itemToUse.Utiliser())
                case _:
                    self._player.AddEffect(*itemToUse.Utiliser())
            # TODO : SUpprimer l'item apres utilisation (del marche pas)

        attackList = []
        enemiToAttack = self.GetEnemiToAttack()
        choice, damage = self.GetAttackPlayerChoice(attackList)
        #print(attackList)
        sleep(TIMETOWAITBETWEENATTACKS*2)
        print(f"Tu attaque {enemiToAttack.GetName()} pour {damage} degats avec {choice}")

    def AskForObjectUse(self):
        if player.GetBag().Empty():
            return False

        if questionary.select("Voulez vous utiliser un objet ?", choices=["Oui", "Non"]).ask() == "None":
            return False
        usableObjectList = self._player.GetUsableObjects()
        objectWithStatsToShow = self.ConvertUsableObjectsToNiceString(usableObjectList)
        objectNames, nameAssociations = self.GetNamesFromItems(usableObjectList)
        #print(objectNames, nameAssociations)
        print(objectWithStatsToShow)
        return nameAssociations[questionary.select("Quel objet veux-tu utiliser ?", choices=objectNames).ask()]

    def ConvertUsableObjectsToNiceString(self, usableObjectList:list[UsableObject]):
        rep = ""
        for item in usableObjectList:
            rep += f"{item.GetName()} --> {item.GetEffectAsString()}\n"
        return rep
    
    def GetNamesFromItems(self, objects:list[Object]):
        repList = []
        repDico = {}
        for item in objects:
            repList.append(item.GetName())
            repDico[item.GetName()] = item
        return repList, repDico

    def EnemiTurn(self):
        if len(self._enemies) == 0:
            print("Plus d'ennemi")
            return
        enemiesToPLay:int = random.randint(0, len(self._enemies))

        for _ in range(enemiesToPLay+1):
            attackingEnemi = self._enemies[random.randint(0, len(self._enemies)-1)]
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

    def GetEnemiToAttack(self, text:str="Quel ennemi voulez-vous attaquer ?"):
        enemies = ""
        enemiNameList = []
        for enemi in self._enemies:
            enemiNameList.append(enemi.GetName())
            enemies += f" {enemi.GetName()} - {enemi.GetHp()} hp\n"
        
        print(enemies)
        choice = questionary.select(text, choices=enemiNameList).ask()
        return self._enemiNames[choice]
    
if __name__ == "__main__":
    player = Player("e")
    enemi = Enemi("r", 10)
    e2 = Enemi("ytrez", 10, [("cacatoutmou", 0)])

    item = Antiseche("caca", 20)
    player.GetBag().AddItem(item)


    fight = Fight(player, [enemi, e2])

    fight.StartFight()