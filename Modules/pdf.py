import os

#Objet représentant un fichier pdf
class Pdf:
  def __init__(self,path):
    #chemin
    self.path = path
    #nom du fichier
    self.name = ".".join(os.path.basename(path).split(".")[:-1])
    
