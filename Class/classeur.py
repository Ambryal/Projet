class Classeur(dict):
  
  class Tag():

    def __init__(self,nom,balise):
      self.nom=nom
      self.baliseDebut="<"+balise+">"
      self.baliseFin="</"+balise+">\n"
      
  tags={
    "article":Tag("","article"),
    "nom":Tag("Nom","preamble"),
    "titre":Tag("Titre","titre"),

    "auteurs":Tag("","auteurs"),
    "auteur":Tag("","auteur"),
    "mail":Tag("Mails des auteurs","mail"),
    "noms":Tag("Noms des auteurs","nom"),
    "univ":Tag("Affiliations des auteurs","affiliation"),

    "abstract":Tag("Abstract","abstract"),
    "intro":Tag("Introduction","introduction"),
    "discu":Tag("Discussion","discussion"),
    "biblio":Tag("Bibliographie","biblio"),
    "conclu":Tag("Conclusion","conclusion"),
    
    "corps":Tag("Corps","corps"),
    }
    
  
  def __init__(self,carnet):
    self.pdf=carnet.pdf

    self["nom"]=self.pdf.name+".pdf"

    self["titre"]=carnet.getTitre()

    self["mail"]=carnet.getMail()

    self["noms"]=carnet.getNom(self["mail"])

    self["univ"]=carnet.getUniv(self["mail"])
    
    self["abstract"]=carnet.getAbstract()

    self["intro"]=carnet.getIntro()

    self["discu"]=carnet.getDiscu()

    self["conclu"]=carnet.getConclu()

    self["biblio"]=carnet.getBiblio()

    self["corps"]=carnet.getCorps()


  def saveAsTxt(self,path):
    s=""
    for i in self:
      if tage[i].nom!="":
        s+=Classeur.tags[i].nom+" : \n\n"
        if type(self[i])==str:
          s+=self[i]
        else:
          for j in self[i]:
            s+=j+"\n"
        s+="\n\n"
      
    self.save(path+"/"+self.pdf.name+".txt",s)

  def balise(self,l):
    s=""
    if len(l)==0:
      pass
    elif type(l[0])==list:
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
        ["titre"],
        ["auteurs",
          [
            ["auteur",
              [["noms",self["noms"][i]],
               ["mail",self["mail"][i]],
               ["univ",self["univ"][i]],
               ]
              ]
           for i in range(len(self["mail"]))]
          ],
        ["abstract"],
        ["intro"],
        ["corps"],
        ["discu"],
        ["conclu"],
        ["biblio"],
        ]
      ]
    self.save(path+"/"+self.pdf.name+".xml",self.balise(syntaxe))


  def save(self,path,valeur):
    file = open (path, 'w', encoding="utf8")
    file.write(valeur)
    file.close()
