
class Bloc(str):
    def __new__(cls, value="", *args, **kwargs):
        return super(Bloc, cls).__new__(cls, value)

    def __init__(self, text="", font=None, size=None, pos=None):
        self.font = font
        self.size = size
        self.pos = pos
        self.text = text

    def fixe(self):
      return Bloc(self.text,self.font,self.size,self.pos)

    def print(self):
        return("\n----------------------------------\n"+
               "Police : "+str(self.font)+"        Taille : "+str(round(self.size))+
               "\n"+self.text)
