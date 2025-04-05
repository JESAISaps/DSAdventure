import click

TIMETOWAITBETWEENATTACKS = .5

def CompareWord(mot1 : str,mot2 : str) -> bool :
    mot1modifie=mot1.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    mot2modifie=mot2.lower().replace("s","").replace("é","e").replace("è","e").replace("'","").replace("ê","e").replace(" ","").replace("(","").replace(")","")
    return mot1modifie == mot2modifie

class CustomChoice(click.Choice):
    def fail(self, value, param=None, ctx=None):
        raise click.BadParameter(
            f"Veuillez choisir parmi : {', '.join(self.choices)}"
        )