from Player import Player, Enemi, Character
from Object import UsableObject, Object, Antiseche
#from Room import FightRoom
import questionary
import random
from time import sleep
from Utils import *
from copy import copy, deepcopy
from colorama import Fore
from colorama import Fore
import math


class Fight:
    def __init__(self, player:Player, enemiList:list[Enemi]):
        self._player:Player = player
        self._enemies:list[Enemi] = enemiList

        #self._enemiNames = {f"{enemi.GetName()} - {enemi.GetHp()} hp":enemi for enemi in enemiList}

    def StartFight(self):
        while self._enemies != [] and self._player.IsAlive(): #On continue tant qu'il y a des ennemis, et que le joueur est vivant.
            self.DoRound()
            if self._player.IsAlive():
                WaitForSpace()

        if self._player.IsAlive():
            #print("Tu peux a present changer de salle.")
            return True
        else:
            #print("nul tu as perdu")
            return False

    def DoRound(self):
        if (self._enemies == []):
            return
            
        self.PlayerTurn()

        self.CheckForKilledEnemy()

        self.EnemiTurn()

        self.EndRound()
        sleep(2)        

    def CheckForKilledEnemy(self):
        enemiList = copy(self._enemies)
        for enemi in enemiList:
            if not enemi.IsAlive():
                self.GivePlayerXp(enemi.GetLevel())
                rewards = self.GetRewardsOnKill(enemi)
                self.AddKillRewardsToPLayer(rewards)
                self.KillEnemy(enemi)

    def GivePlayerXp(self, level):
        xpToAdd = math.ceil(self._player.GetXpCaps(level) * random.uniform(.2, .4)) # La quantite d'exp depend du niveau de l'enemi
        self._player.AjouterXp(xpToAdd)
        print(f"Tu as obtenu {Fore.BLUE}{xpToAdd}{Fore.WHITE} points d'exp !")

    def GetRewardsOnKill(self, enemi:Enemi):
        dropTable = enemi.GetDropTable()
        toDrop = []
        for item in dropTable:
            if random.randint(0, 150) <= dropTable[item]:
                if item.objectType == ObjectType.Money: # On ajoute deja l'argent, puis le reste.
                    self._player.AddItem(item)
                    print(f'Tu as gagné {item.GetAmount()}€')
                
                else:
                    toDrop.append(item)
        
        return deepcopy(toDrop)
    
    def AddKillRewardsToPLayer(self, rewards:list[Object]):
        if len(rewards) <= self._player.GetBag().GetEmptySpacesNb():
            for item in rewards:
                self._player.AddItem(item)
                print(f"Tu as obtenu {Fore.BLUE + item.GetName() + Fore.RESET}.")
        else:

            print("Tu n'as pas assez de place pour tous les objets.")
            sleep(TIMETOWAITBETWEENATTACKS/2)
            
            while(self._player.GetBag().GetEmptySpacesNb() > 0):
                rewardDico = {item.GetName():item for item in rewards}
                flush_stdin()
                item = questionary.select("Quel objet veux-tu prendre ?", choices=rewardDico.keys(), style=QUESTIONARYSTYLE).ask()
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
        print(f"Tu as actuellement {self._player.GetHp()} hp")
        itemToUse:UsableObject = self.AskForObjectUse()
        if itemToUse == "Annuler":
            pass
        elif itemToUse != False:
            self.UseObject(itemToUse)

        attackList = []
        enemiToAttack = self.GetEnemiToAttack()
        choice, attack= self.GetAttackPlayerChoice(attackList)
        damage = 0

        if not self.GetTouched(self._player, enemiToAttack):
            print(f"{enemiToAttack.GetName()} a esquivé ton attaque.")
            return
        for attaque in attack:
            match attaque:
                case AttackStats.Degats:
                    damage = attack[attaque]
                case Effect.AugmentationDegatSelf:
                    self._player.AddEffect(attaque, attack[attaque])
                case Effect.AnnulationAttaqueSelf:
                    self._player.AddEffect(attaque, attack[attaque])
                case _: # Si on met juste un effet sur l'ennemi
                    enemiToAttack.AddEffect(attaque, attack[attaque])
        sleep(TIMETOWAITBETWEENATTACKS*2)
        damageDone = enemiToAttack.TakeDamage(damage)
        print(f"Tu attaque {enemiToAttack.GetName()} pour {Fore.GREEN} {damageDone} {Fore.RESET} degats avec {choice}")

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
        self._player.RemoveItem(itemToUse)

    def AskForObjectUse(self):
        if self._player.GetUsableObjects() == []:
            return False

        self.ShowEnemies()
        flush_stdin()

        if questionary.select("Voulez vous utiliser un objet ?", choices=CHOICEYESORNO, style=QUESTIONARYSTYLE).ask() == "Non":
            return False
        usableObjectList = self._player.GetUsableObjects()
        objectWithStatsToShow = self.ConvertUsableObjectsToNiceString(usableObjectList)
        objectNames, nameAssociations = self.GetNamesFromItems(usableObjectList)
        print(objectWithStatsToShow)
        flush_stdin()
        objectNames.append("Annuler")
        return nameAssociations[questionary.select("Quel objet veux-tu utiliser ?", choices=objectNames, style=QUESTIONARYSTYLE).ask()]

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
            #print("Plus d'ennemi")
            return
        enemiesToPLay:int = random.randint(0, len(self._enemies))

        for _ in range(enemiesToPLay+1):
            attackingEnemi = self._enemies[random.randint(0, len(self._enemies)-1)]
            isTouched = self.GetTouched(attackingEnemi, self._player)
            if attackingEnemi.GetAttackDelay() == 0 and isTouched:
                attackName, damage = attackingEnemi.GetNextEnnemiAttack()
                sleep(TIMETOWAITBETWEENATTACKS)
                damageDone = self._player.TakeDamage(damage)
                print(f"{attackingEnemi.GetName()} t'attaque avec {attackName} pour {Fore.RED} {damageDone} {Fore.RESET} degats !")
            elif not isTouched:
                print(f"Tu as esquivé l'attaque de {attackingEnemi.GetName()}")
            else:
                print(f"{attackingEnemi.GetName()} ne peut pas attaquer.")
                attackingEnemi.ReduceAttackDelayAfterTry()

    def GetTouched(self, attacker:Character, victim:Character):
        return random.randint(0,100) <= attacker.GetPrecision() * ((100-victim.GetEvasion())/100)

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
        flush_stdin()
        choice = questionary.select("Quelle attaque voulez vous utiliser ?", choices=attackList, instruction=" ", style=QUESTIONARYSTYLE).ask()
        return choice, playerAttacks[choice]

    def GetEnemiToAttack(self, text:str="Quel ennemi voulez-vous attaquer ?"):
        enemiNames = {f"{enemi.GetName()} - {enemi.GetHp()} hp":enemi for enemi in self._enemies}

        flush_stdin()
        choice = questionary.select(text, choices=enemiNames.keys(), style=QUESTIONARYSTYLE).ask()
        return enemiNames[choice]
    
    def ShowEnemies(self):
        enemies = "Les ennemis:\n"
        for enemi in self._enemies:
            enemies += f" {enemi.GetName()} - {enemi.GetHp()} hp\n"
        print(enemies)
    
    def KillEnemy(self, enemi):
        self._enemies.remove(enemi)
    
if __name__ == "__main__":
    crotter = Player("e")
    crotter.GetBag().bagSize = 2
    enemi = Enemi("r", 10, [("cacatoutmou", 0)])
    e2 = Enemi("ytrez", 10, [("cacatoutmou", 0)])

    #item = Antiseche("caca", 20)
    #crotter.AddItem(item)


    fight = Fight(crotter, [enemi, e2])

    fight.StartFight()