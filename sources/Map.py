from Room import FightRoom, CodeName, Menu, Sphinx, Morpion, Conseil, Integrale, Shop
from Player import Enemi


class Map:

    def __init__(self):

        self.petitStartStats = ("Petit Boss", 25, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 2)
        self.babaStartStats = ("Baba Boss", 30, [("Fausses révisions", 5), ("Calcul lourd", 3), ("Lancer de stylo", 10)], 2)
        self.totoStartStats = ("Toto Boss", 1, [("ODG", 100)], 2, -10000000000) # On baisse beaucoup l'esquive de depart de Toto, pour etre sur de le toucher
        self.barceloStats = ("Baba", 10, [("Norme",2), ("Regard Percant",1), ("Espace métrique",5)], 2)
        self.olivStats = ("Oliv", 15, [("ODG", 6), ("Outils Maths", 5), ("Vue de l'esprit", 20)], 4)
        self.petitStats = ("Le Cam", 150, [("Norme",40), ("Regard Percant",30), ("Espace métrique",50)], 7)
        self.bigMathsPetitStats = ("Petit", 20, [("Norme",10), ("Regard Percant",5), ("Espace métrique",15)], 5)
        self.bigMathBabaStats = ("Baba", 20, [("Norme",10), ("Regard Percant",7), ("Espace métrique",9)], 5)
        self.deschampsStats = ("Didier", 50, [("Moment cinetique", 20), ("Coupe du monde 98", 30), ("Pied de biche", 50)], 6)
        self.diasStats = ("Nath", 120, [("Regard Mechant", 20), ("DS de l'annee derniere", 25), ("Formule fausse", 30)], 8)
        self.communsPetitStats = ("Petit", 200, [("Integrale triple", 50), ("Compact simple", 40), ("Discussion serieuse", 55)], 8)
        self.communsBabaStats = ("Baba", 200, [("Trivial", 45), ("Au tableau", 25), ("Lancer de crayon",40), ("Detachement de cheveux",1000)], 8)
        self.communsOlivStats = ("Oliv", 200, [("ODG", 50), ("Boite a outils", 60)], 8)

        self.menu=Menu("1ère année")
        self.shop=Shop("Shop")
        self.defiCodeName=CodeName()
        self.defiSphinx=Sphinx()
        self.defiMorpion=Morpion()
        self.defiIntegrale=Integrale()

        self.petitStart = Enemi(*self.petitStartStats)
        self.babaStart = Enemi(*self.babaStartStats)
        self.totoStart = Enemi(*self.totoStartStats)
        self.trioInfernalRoom=FightRoom([self.petitStart,self.babaStart, self.totoStart], "Trio Infernal")
        self.trioInfernalRoomVide=FightRoom([], "Salle Vide")

        self.barcelo = Enemi(*self.barceloStats)
        self.barceloRoom=FightRoom([self.barcelo], "DS nombres complexes")

        self.oliv = Enemi(*self.olivStats)
        self.olivRoom=FightRoom([self.oliv], "Cours éléctrique")

        self.petit = Enemi(*self.petitStats)
        self.petitRoom=FightRoom([self.petit], "Espaces Normés")

        self.bigMathsPetit = Enemi(*self.bigMathsPetitStats)
        self.bigMathBaba = Enemi(*self.bigMathBabaStats)
        self.bigMaths=FightRoom([self.bigMathBaba,self.bigMathsPetit], "Big Math")

        self.salletranquille=FightRoom([], "Interruptions pédagogiques")

        self.deschamps = Enemi(*self.deschampsStats)
        self.mecaSol=FightRoom([self.deschamps], "Mecanique Solide")

        self.dias = Enemi(*self.diasStats)
        self.thermo=FightRoom([self.dias], "Thermique")

        self.communsPetit = Enemi(*self.communsPetitStats)
        self.communsBaba = Enemi(*self.communsBabaStats)
        self.communsOliv = Enemi(*self.communsOlivStats)
        self.communs=FightRoom([self.communsPetit,self.communsBaba, self.communsOliv], "Communs")

        self.conseil=Conseil()

        self.menu.SetVoisins(est=self.shop)
        self.trioInfernalRoom.SetVoisins(est=self.barceloRoom)
        self.trioInfernalRoomVide.SetVoisins(est=self.barceloRoom)

        self.barceloRoom.SetVoisins(est=self.defiCodeName, sud=self.olivRoom)
        self.olivRoom.SetVoisins(ouest=self.petitRoom, sud=self.bigMaths, passage=self.salletranquille)
        self.petitRoom.SetVoisins(ouest=self.defiSphinx, est=self.olivRoom)
        self.defiSphinx.SetVoisins(est=self.petitRoom)
        self.bigMaths.SetVoisins(sud=self.salletranquille)
        self.salletranquille.SetVoisins(ouest=self.mecaSol)
        self.mecaSol.SetVoisins(nord=self.thermo, sud=self.defiIntegrale, passage=self.conseil)
        self.defiIntegrale.SetVoisins(nord=self.mecaSol)
        self.thermo.SetVoisins(est=self.communs)
        self.communs.SetVoisins(nord=self.defiMorpion, sud=self.conseil)
        self.shop.SetVoisins(est=self.trioInfernalRoom)
        self.defiCodeName.SetVoisins(ouest = self.barceloRoom)
        self.defiMorpion.SetVoisins(sud = self.communs)