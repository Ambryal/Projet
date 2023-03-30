from tag import Tag

class Classeur(dict):

  tags={
    "nom":Tag("Nom","<balise>"),
    "titre":Tag("Titre","<balise>"),
    }
    
  
  def __init__(self,carnet):
    self.pdf=carnet.pdf

    self["nom"]=self.pdf.name

    self["titre"]=carnet.getTitre()

  def saveAsTxt(self,path="test"):

    s=""
    for i in self:
      s+=Classeur.tags[i].nom+" : \n\n"+self[i]+"\n\n\n"
      
    self.save(path+".txt",s)


  def save(self,path,valeur):
    file = open (path, 'w', encoding="utf8")
    file.write(valeur)
    file.close()
