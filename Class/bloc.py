"""
Objet héritant de String modélisant les éléments élémentaires manipulés par
le programme.
"""
class Bloc(str):
    #Héritage de String
    def __new__(cls, value="", *args, **kwargs):
        return super(Bloc, cls).__new__(cls, value)

    def __init__(self, text="", font=None, size=None, pos=None):
        #Police
        self.font = font
        #Taille de la police
        self.size = size
        #Position
        self.pos = pos
        #Texte
        self.text = text

    #Méthode appelée lors de la fin du "modelage" de l'objet, pour qu'il
    #puisse effectivement être utilisé comme une chaîne par la suite.
    def fixe(self):
      return Bloc(self.text,self.font,self.size,self.pos)

    #Affichage
    def print(self):
        return("\n----------------------------------\n"+
               "Police : "+str(self.font)+"        Taille : "+str(round(self.size))+
               "\n"+self.text)

