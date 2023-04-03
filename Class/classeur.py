class Classeur(dict):
  
  class Tag():

    def __init__(self,nom,balise):
      self.nom=nom
      self.baliseDebut="<"+balise+">\n"
      self.baliseFin="</"+balise+">\n"
    
  tags={
    "article":Tag("","article"),
    "nom":Tag("Nom","preambule"),
    "titre":Tag("Titre","titre"),
    }
    
  
  def __init__(self,carnet):
    self.pdf=carnet.pdf

    self["nom"]=self.pdf.name

    self["titre"]=carnet.getTitre()


  def saveAsTxt(self,path):
    s=""
    for i in self:
      s+=Classeur.tags[i].nom+" : \n\n"+self[i]+"\n\n\n"
      
    self.save(path+"/"+self.pdf.name+".txt",s)

  def balise(self,l):
    s=""
    if type(l[0])==list:
      for i in l:
        s+=self.balise(i)
    else:
      t=Classeur.tags[l[0]]
      s+=t.baliseDebut
      if len(l)==1:
        s+=self[l[0]]
      elif type(l[1])==str:
        s+=l[1]
      else:
        s+=self.balise(l[1])
      s+=t.baliseFin
    return s

  def saveAsXml(self,path):
    syntaxe=[
      "article",[
        ["nom"],
        ["titre"]
        ]
      ]
    self.save(path+"/"+self.pdf.name+".xml",self.balise(syntaxe))


  def save(self,path,valeur):
    file = open (path, 'w', encoding="utf8")
    file.write(valeur)
    file.close()
