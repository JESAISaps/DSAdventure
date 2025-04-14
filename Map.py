from Room import FightRoom, CodeName, Menu, Sphinx, Morpion, Conseil, Integrale, Room,Shop
from Player import Enemi


class Map:

    def __init__(self):
        #menuStats=Menu("1ère année")
        #shopStats=Shop("Shop")
        #defiVoyance=CodeName()
        #defiOneShot=Sphinx()
        #defiLunettes=Morpion()
        #defiDoubleCoup=Integrale()
        self.petitStartStats = ("Petit Boss", 5, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 3)
        self.babaStartStats = ("Baba Boss", 10, [("Fausses révisions", 5), ("Calcul lourd", 3), ("Lancer de stylo", 10)], 3)
        self.totoStartStats = ("Toto Boss", 1, [("ODG", 100)], 3)
        #trioInfernalRoomStats=FightRoom([petitStart,babaStart, totoStart])
        #trioInfernalRoomVideStats=FightRoom([])
        self.barceloStats = ("Baba", 10, [("Norme",2), ("Regard Percant",1), ("Espace métrique",5)], 2)
        #barceloRoomStats=FightRoom([barcelo])
        self.olivStats = ("Oliv", 15, [("ODG", 10), ("Outils Maths", 5), ("Vue de l'esprit", 50)], 4)
        #olivRoomStats=FightRoom([oliv])
        self.petitStats = ("Le Cam", 100, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 7)
        #petitRoomStats=FightRoom([petit])
        self.bigMathsPetitStats = ("Petit", 20, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 5)
        self.bigMathBabaStats = ("Baba", 20, [("Norme",2), ("Regard Percant",1), ("Espace métrique",5)], 5)
        #bigMathsStats=FightRoom([bigMathBaba,bigMathsPetit])
        #salletranquilleStats=FightRoom([])
        self.deschampsStats = ("Didier", 50, [("Moment cinetique", 20), ("Coupe du monde 98", 15), ("Pied de biche", 50)], 6)
        #mecaSolStats=FightRoom([deschamps])
        self.diasStats = ("Nath", 120, [("Regard Mechant", 20), ("DS de l'annee derniere", 10), ("Formule fausse", 10)], 8)
        #thermoStats=FightRoom([dias])
        self.communsPetitStats = ("Petit", 150, [("Integrale triple", 50), ("Compact simple", 40), ("Discussion serieuse", 50)], 8)
        self.communsBabaStats = ("Baba", 150, [("Trivial", 45), ("Au tableau", 25), ("Lancer de crayon",35), ("Detachement de cheveux",1000)], 8)
        self.communsOlivStats = ("Oliv", 150, [("ODG", 50), ("", 40)], 8)
        #communs=FightRoom([communsPetit,communsBaba, communsOliv])
        #conseil=Conseil()
        #menu.SetVoisins(est=shop)
        #trioInfernalRoom.SetVoisins(est=barceloRoom)
        #trioInfernalRoomVide.SetVoisins(est=barceloRoom)
        #barceloRoom.SetVoisins(est=defiVoyance, sud=olivRoom)
        #olivRoom.SetVoisins(ouest=petitRoom, sud=bigMaths, passage=salletranquille)
        #petitRoom.SetVoisins(ouest=defiOneShot, est=olivRoom)
        #defiOneShot.SetVoisins(est=petitRoom)
        #bigMaths.SetVoisins(sud=salletranquille)
        #salletranquille.SetVoisins(ouest=mecaSol)
        #mecaSol.SetVoisins(nord=thermo, sud=defiDoubleCoup, passage=conseil)
        #defiDoubleCoup.SetVoisins(nord=mecaSol)
        #thermo.SetVoisins(est=communs)
        #communs.SetVoisins(nord=defiLunettes, sud=conseil)
        #shop.SetVoisins(est=trioInfernalRoom)
        #defiVoyance.SetVoisins(ouest = barceloRoom)

    #def initMap(self):

        self.menu=Menu("1ère année")
        self.shop=Shop("Shop")
        self.defiVoyance=CodeName()
        self.defiOneShot=Sphinx()
        self.defiLunettes=Morpion()
        self.defiDoubleCoup=Integrale()

        self.petitStart = Enemi(*self.petitStartStats)
        self.babaStart = Enemi(*self.babaStartStats)
        self.totoStart = Enemi(*self.totoStartStats)
        self.trioInfernalRoom=FightRoom([self.petitStart,self.babaStart, self.totoStart])
        self.trioInfernalRoomVide=FightRoom([])

        self.barcelo = Enemi(*self.barceloStats)
        self.barceloRoom=FightRoom([self.barcelo])

        self.oliv = Enemi(*self.olivStats)
        self.olivRoom=FightRoom([self.oliv])

        self.petit = Enemi(*self.petitStats)
        self.petitRoom=FightRoom([self.petit])

        self.bigMathsPetit = Enemi(self.bigMathsPetitStats)
        self.bigMathBaba = Enemi(*self.bigMathBabaStats)
        self.bigMaths=FightRoom([self.bigMathBaba,self.bigMathsPetit])

        self.salletranquille=FightRoom([])

        self.deschamps = Enemi(*self.deschampsStats)
        self.mecaSol=FightRoom([self.deschamps])

        self.dias = Enemi(*self.diasStats)
        self.thermo=FightRoom([self.dias])

        self.communsPetit = Enemi(*self.communsPetitStats)
        self.communsBaba = Enemi(*self.communsBabaStats)
        self.communsOliv = Enemi(*self.communsOlivStats)
        self.communs=FightRoom([self.communsPetit,self.communsBaba, self.communsOliv])

        self.conseil=Conseil()

        self.menu.SetVoisins(est=self.shop)
        self.trioInfernalRoom.SetVoisins(est=self.barceloRoom)
        self.trioInfernalRoomVide.SetVoisins(est=self.barceloRoom)

        self.barceloRoom.SetVoisins(est=self.defiVoyance, sud=self.olivRoom)
        self.olivRoom.SetVoisins(ouest=self.petitRoom, sud=self.bigMaths, passage=self.salletranquille)
        self.petitRoom.SetVoisins(ouest=self.defiOneShot, est=self.olivRoom)
        self.defiOneShot.SetVoisins(est=self.petitRoom)
        self.bigMaths.SetVoisins(sud=self.salletranquille)
        self.salletranquille.SetVoisins(ouest=self.mecaSol)
        self.mecaSol.SetVoisins(nord=self.thermo, sud=self.defiDoubleCoup, passage=self.conseil)
        self.defiDoubleCoup.SetVoisins(nord=self.mecaSol)
        self.thermo.SetVoisins(est=self.communs)
        self.communs.SetVoisins(nord=self.defiLunettes, sud=self.conseil)
        self.shop.SetVoisins(est=self.trioInfernalRoom)
        self.defiVoyance.SetVoisins(ouest = self.barceloRoom)