from Room import FightRoom, CodeName, Menu, Sphinx, Morpion, Conseil, Integrale, Room
from Player import Enemi

depart=Menu("1ère année")
defiVoyance=CodeName("CodeName")
defiOneShot=Sphinx("Sphinx")
defiLunettes=Morpion("Morpion")
defiDoubleCoup=Integrale("Integrale")

petitStart = Enemi("Petit Boss", 5, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
babaStart = Enemi("Baba Boss", 10, [("Fausses révisions", 5), ("Calcul lourd", 3), ("Lancer de stylo", 10)])
totoStart = Enemi("Toto Boss", 1, [("ODG", 100)])
trioInfernalRoom=FightRoom([petitStart,babaStart, totoStart])

barcelo = Enemi("Baba", 10, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
barceloRoom=FightRoom(["Barcelo"])

oliv = Enemi("Oliv", 10, [("ODG", 10), ("Outils Maths", 5), ("Vue de l'esprit", 50)])
olivRoom=FightRoom(["Torinesi"])

petit = Enemi("Le Cam", 50, [("Norme",3), ("Regard Percant",1), ("Espace métrique",10)])
petitRoom=FightRoom(["Petit"])

bigMathsPetit = Enemi("Petit")
bigMathBaba = Enemi("Baba")
bigMaths=FightRoom([bigMathBaba,bigMathsPetit])

salletranquille=FightRoom("Salle tranquille", [])

deschamps = Enemi("Didier", 100, [("Moment cinetique", 20), ("Coupe du monde 98", 15), ("Pied de biche", 50)])
mecaSol=FightRoom(["Deschamps"])

dias = Enemi("Nath", 100, [("Regard Mechant", 20), ("DS de l'annee derniere", 10), ("Formule fausse", 10)])
thermo=FightRoom(["Nathalie Dias"])

communsPetit = Enemi("Petit", 200, [("Integrale triple", 50), ("Compact simple", 40), ("Discussion serieuse", 50)])
communsBaba = Enemi("Baba", 200, [("Trivial", 45), ("Au tableau", 25), ("Lancer de crayon",35), ("Detachement de cheveux",1000)])
communsOliv = Enemi("Oliv", 200, [("ODG", 50), ("", 40)])
communs=FightRoom(["Petit","Barcelo", "Torinesi"])

conseil=Conseil()

depart.SetVoisins(est = trioInfernalRoom)
trioInfernalRoom.SetVoisins(est = barcelo)
barceloRoom.SetVoisins(est = defiVoyance, sud = oliv)
olivRoom.SetVoisins(ouest = petit, sud = bigMaths, passage=salletranquille)
petitRoom.SetVoisins(ouest = defiOneShot, est = oliv)
defiOneShot.SetVoisins(est=petit)
bigMaths.SetVoisins(sud = salletranquille)
salletranquille.SetVoisins(ouest = mecaSol)
mecaSol.SetVoisins(nord = thermo, sud = defiDoubleCoup, passage = conseil)
defiDoubleCoup.SetVoisins(nord = mecaSol)
thermo.SetVoisin(est = communs)
communs.SetVoisins(nord = defiLunettes, sud = conseil)
