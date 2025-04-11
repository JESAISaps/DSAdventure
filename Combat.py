from Player import Player, Enemi
from Object import UsableObject, Object, Antiseche
#from Room import FightRoom
import questionary
import random
from time import sleep
from Utils import TIMETOWAITBETWEENATTACKS, Effect, AttackStats
from copy import copy, deepcopy

class Fight:
    def __init__(self, player:Player, enemiList:list[Enemi]):
        self._player:Player = player
        self._enemies:list[Enemi] = enemiList

        self._enemiNames = {enemi.GetName():enemi for enemi in enemiList}

    def StartFight(self):
        while self._enemies != [] and self._player.IsAlive(): #On continue tant qu'il y a des ennemis, et que le joueur est vivant.
            self.DoRound()

        if self._player.IsAlive():
            print("Tu peux a present changer de salle.")
            return True
            # TODO: Donner les recompenses, et terminer le combat.
        else:
            print("nul tu as perdu")
            return False
            # TODO: Le joueur est mort, faut recommencer.

    def DoRound(self):
        self.PlayerTurn()

        self.CheckForKilledEnemy()

        self.EnemiTurn()

        self.EndRound()

    def CheckForKilledEnemy(self):
        enemiList = copy(self._enemies)
        for enemi in enemiList:
            if not enemi.IsAlive():
                rewards = self.GetRewardsOnKill(enemi)
                self.AddKillRewardsToPLayer(rewards)
                self.KillEnemy(enemi)

    def GetRewardsOnKill(self, enemi:Enemi):
        dropTable = enemi.GetDropTable()
        toDrop = []
        for item in dropTable:
            if random.randint(0, 150) <= dropTable[item]:
                toDrop.append(item)
        
        return deepcopy(toDrop)
    
    def AddKillRewardsToPLayer(self, rewards:list[Object]):
        if len(rewards) <= self._player.GetBag().GetEmptySpacesNb():
            for item in rewards:
                self._player.AddItem(item)
                print(f"Tu as obtenu {item.GetName()}.")
        else:
            print("Tu n'as pas assez de place pour tous les objets.")
            sleep(TIMETOWAITBETWEENATTACKS/2)
            while(self._player.GetBag().GetEmptySpacesNb() > 0):
                rewardDico = {item.GetName():item for item in rewards}
                item = questionary.select("Quel objet veux- tu prendre ?", choices=rewardDico.keys()).ask()
                self._player.AddItem(rewardDico[item])
                rewards.remove(rewardDico[item])
                
        

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
            self.UseObject(itemToUse)

        attackList = []
        enemiToAttack = self.GetEnemiToAttack()
        choice, attack= self.GetAttackPlayerChoice(attackList)
        damage = attack[AttackStats.Degats]
        sleep(TIMETOWAITBETWEENATTACKS*2)
        print(f"Tu attaque {enemiToAttack.GetName()} pour {damage} degats avec {choice}")
        enemiToAttack.TakeDamage(damage)

    def UseObject(self, itemToUse:UsableObject):
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
            # TODO : Supprimer l'item apres utilisation (del marche pas)

    def AskForObjectUse(self):
        if self._player.GetUsableObjects() == []:
            return False

        if questionary.select("Voulez vous utiliser un objet ?", choices=["Oui", "Non"]).ask() == "Non":
            return False
        usableObjectList = self._player.GetUsableObjects()
        objectWithStatsToShow = self.ConvertUsableObjectsToNiceString(usableObjectList)
        objectNames, nameAssociations = self.GetNamesFromItems(usableObjectList)
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
        playerAttacks:dict[str:dict[AttackStats.Degats:int]] = self._player.GetAttacks()
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
        return choice, playerAttacks[choice]

    def GetEnemiToAttack(self, text:str="Quel ennemi voulez-vous attaquer ?"):
        enemies = ""
        enemiNameList = []
        for enemi in self._enemies:
            enemiNameList.append(enemi.GetName())
            enemies += f" {enemi.GetName()} - {enemi.GetHp()} hp\n"
        
        print(enemies)
        choice = questionary.select(text, choices=enemiNameList).ask()
        return self._enemiNames[choice]
    
    def KillEnemy(self, enemi):
        self._enemies.remove(enemi)
    
if __name__ == "__main__":
    crotter = Player("e")
    crotter.GetBag().bagSize = 2
    enemi = Enemi("r", 10)
    e2 = Enemi("ytrez", 10, [("cacatoutmou", 0)])

    item = Antiseche("caca", 20)
    crotter.AddItem(item)


    fight = Fight(crotter, [enemi, e2])

    fight.StartFight()