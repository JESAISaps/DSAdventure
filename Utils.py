def CompareWord(mot1 : str,mot2 : str) -> bool :
    mot1modifie=mot1.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","")
    mot2modifie=mot2.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","")
    return mot1modifie == mot2modifie
