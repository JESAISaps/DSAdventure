from Room import FightRoom, CodeName, Menu, Sphinx, Morpion, Conseil, Integrale, Room,Shop
from Player import Enemi





#menuStats=Menu("1ère année")
#shopStats=Shop("Shop")
#defiVoyance=CodeName()
#defiOneShot=Sphinx()
#defiLunettes=Morpion()
#defiDoubleCoup=Integrale()
petitStartStats = ("Petit Boss", 5, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 3)
babaStartStats = ("Baba Boss", 10, [("Fausses révisions", 5), ("Calcul lourd", 3), ("Lancer de stylo", 10)], 3)
totoStartStats = ("Toto Boss", 1, [("ODG", 100)], 3)
#trioInfernalRoomStats=FightRoom([petitStart,babaStart, totoStart])
#trioInfernalRoomVideStats=FightRoom([])
barceloStats = ("Baba", 10, [("Norme",2), ("Regard Percant",1), ("Espace métrique",5)], 2)
#barceloRoomStats=FightRoom([barcelo])
olivStats = ("Oliv", 15, [("ODG", 10), ("Outils Maths", 5), ("Vue de l'esprit", 50)], 4)
#olivRoomStats=FightRoom([oliv])
petitStats = ("Le Cam", 100, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 7)
#petitRoomStats=FightRoom([petit])
bigMathsPetitStats = ("Petit", 20, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)], 5)
bigMathBabaStats = ("Baba", 20, [("Norme",2), ("Regard Percant",1), ("Espace métrique",5)], 5)
#bigMathsStats=FightRoom([bigMathBaba,bigMathsPetit])
#salletranquilleStats=FightRoom([])
deschampsStats = ("Didier", 50, [("Moment cinetique", 20), ("Coupe du monde 98", 15), ("Pied de biche", 50)], 6)
#mecaSolStats=FightRoom([deschamps])
diasStats = ("Nath", 120, [("Regard Mechant", 20), ("DS de l'annee derniere", 10), ("Formule fausse", 10)], 8)
#thermoStats=FightRoom([dias])
communsPetitStats = ("Petit", 150, [("Integrale triple", 50), ("Compact simple", 40), ("Discussion serieuse", 50)], 8)
communsBabaStats = ("Baba", 150, [("Trivial", 45), ("Au tableau", 25), ("Lancer de crayon",35), ("Detachement de cheveux",1000)], 8)
communsOlivStats = ("Oliv", 150, [("ODG", 50), ("", 40)], 8)
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

def initMap():

    global menu, shop, defiVoyance, defiOneShot, defiLunettes, defiDoubleCoup
    global trioInfernalRoom, trioInfernalRoomVide, barceloRoom, olivRoom, petitRoom, bigMaths
    global salletranquille, mecaSol, thermo, communs, conseil
    global petitStart, babaStart, totoStart, barcelo, oliv, petit, bigMathBaba, bigMathsPetit
    global deschamps, dias, communsBaba, communsOliv, communsPetit
    
    menu=Menu("1ère année")
    shop=Shop("Shop")
    defiVoyance=CodeName()
    defiOneShot=Sphinx()
    defiLunettes=Morpion()
    defiDoubleCoup=Integrale()

    petitStart = Enemi(*petitStartStats)
    babaStart = Enemi(*babaStartStats)
    totoStart = Enemi(*totoStartStats)
    trioInfernalRoom=FightRoom([petitStart,babaStart, totoStart])
    trioInfernalRoomVide=FightRoom([])

    barcelo = Enemi(*barceloStats)
    barceloRoom=FightRoom([barcelo])

    oliv = Enemi(*olivStats)
    olivRoom=FightRoom([oliv])

    petit = Enemi(*petitStats)
    petitRoom=FightRoom([petit])

    bigMathsPetit = Enemi(bigMathsPetitStats)
    bigMathBaba = Enemi(*bigMathBabaStats)
    bigMaths=FightRoom([bigMathBaba,bigMathsPetit])

    salletranquille=FightRoom([])

    deschamps = Enemi(*deschampsStats)
    mecaSol=FightRoom([deschamps])

    dias = Enemi(*diasStats)
    thermo=FightRoom([dias])

    communsPetit = Enemi(*communsPetitStats)
    communsBaba = Enemi(*communsBabaStats)
    communsOliv = Enemi(*communsOlivStats)
    communs=FightRoom([communsPetit,communsBaba, communsOliv])

    conseil=Conseil()

    menu.SetVoisins(est=shop)
    trioInfernalRoom.SetVoisins(est=barceloRoom)
    trioInfernalRoomVide.SetVoisins(est=barceloRoom)

    barceloRoom.SetVoisins(est=defiVoyance, sud=olivRoom)
    olivRoom.SetVoisins(ouest=petitRoom, sud=bigMaths, passage=salletranquille)
    petitRoom.SetVoisins(ouest=defiOneShot, est=olivRoom)
    defiOneShot.SetVoisins(est=petitRoom)
    bigMaths.SetVoisins(sud=salletranquille)
    salletranquille.SetVoisins(ouest=mecaSol)
    mecaSol.SetVoisins(nord=thermo, sud=defiDoubleCoup, passage=conseil)
    defiDoubleCoup.SetVoisins(nord=mecaSol)
    thermo.SetVoisins(est=communs)
    communs.SetVoisins(nord=defiLunettes, sud=conseil)
    shop.SetVoisins(est=trioInfernalRoom)
    defiVoyance.SetVoisins(ouest = barceloRoom)