from Room import FightRoom, CodeName, Menu, Sphinx, Morpion, Conseil, Integrale, Room,Shop
from Player import Enemi
import graphviz 

menu=Menu("1ère année")
shop=Shop("Shop")
defiVoyance=CodeName()
defiOneShot=Sphinx()
defiLunettes=Morpion()
defiDoubleCoup=Integrale()

petitStart = Enemi("Petit Boss", 5, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
babaStart = Enemi("Baba Boss", 10, [("Fausses révisions", 5), ("Calcul lourd", 3), ("Lancer de stylo", 10)])
totoStart = Enemi("Toto Boss", 1, [("ODG", 100)])
trioInfernalRoom=FightRoom([petitStart,babaStart, totoStart])
trioInfernalRoomVide=FightRoom([])

barcelo = Enemi("Baba", 10, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
barceloRoom=FightRoom([barcelo])

oliv = Enemi("Oliv", 10, [("ODG", 10), ("Outils Maths", 5), ("Vue de l'esprit", 50)])
olivRoom=FightRoom([oliv])

petit = Enemi("Le Cam", 50, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
petitRoom=FightRoom([petit])

bigMathsPetit = Enemi("Petit")
bigMathBaba = Enemi("Baba")
bigMaths=FightRoom([bigMathBaba,bigMathsPetit])

salletranquille=FightRoom([])

deschamps = Enemi("Didier", 100, [("Moment cinetique", 20), ("Coupe du monde 98", 15), ("Pied de biche", 50)])
mecaSol=FightRoom([deschamps])

dias = Enemi("Nath", 100, [("Regard Mechant", 20), ("DS de l'annee derniere", 10), ("Formule fausse", 10)])
thermo=FightRoom([dias])

communsPetit = Enemi("Petit", 200, [("Integrale triple", 50), ("Compact simple", 40), ("Discussion serieuse", 50)])
communsBaba = Enemi("Baba", 200, [("Trivial", 45), ("Au tableau", 25), ("Lancer de crayon",35), ("Detachement de cheveux",1000)])
communsOliv = Enemi("Oliv", 200, [("ODG", 50), ("", 40)])
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