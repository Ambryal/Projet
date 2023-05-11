
"""
Objet héritant de la classe Dict résumant un pdf sous forme Balise -> Valeur
"""

class Classeur(dict):

  #Objet Tag représentant une balise
  class Tag():

    def __init__(self,nom,balise):
      self.nom=nom
      self.baliseDebut="<"+balise+">"
      self.baliseFin="</"+balise+">\n"

  #Liste des balises
  tags={
    "article":Tag("","article"),
    "nom":Tag("Nom","preamble"),
    "titre":Tag("Titre","titre"),

    "auteurs":Tag("","auteurs"),
    "auteur":Tag("","auteur"),
    "mail":Tag("Mails des auteurs","mail"),
    "noms":Tag("Noms des auteurs","name"),
    "univ":Tag("Affiliations des auteurs","affiliation"),

    "abstract":Tag("Abstract","abstract"),
    "intro":Tag("Introduction","introduction"),
    "discu":Tag("Discussion","discussion"),
    "aknow":Tag("Aknowledgements","aknowledgements"),
    "biblio":Tag("Bibliographie","biblio"),
    "conclu":Tag("Conclusion","conclusion"),
    
    "corps":Tag("Corps","corps"),
    }
    
  
  def __init__(self,carnet):
    self.pdf=carnet.pdf

    #Création de toutes les valeurs dés l'initialisation de l'objet
    
    self["nom"]=self.pdf.name+".pdf"

    self["titre"]=carnet.getTitre()

    self["mail"]=carnet.getMail()

    self["noms"]=carnet.getNom(self["mail"])

    self["univ"]=carnet.getUniv(self["mail"])
    
    self["abstract"]=carnet.getAbstract()

    self["intro"]=carnet.getIntro()

    self["biblio"]=carnet.getBiblio()

    self["discu"]=carnet.getDiscu()
    
    self["aknow"]=carnet.getAknow()
    
    self["conclu"]=carnet.getConclu()

    self["corps"]=carnet.getCorps()

  #Exportation au format txt
  def saveAsTxt(self,path):
    s=""
    for i in ["nom",
              "titre",
              "noms",
              "mail",
              "univ",
              "abstract",
              "intro",
              "corps",
              "discu",
              "conclu",
              "biblio"
              ]:
      s+="-----------------"+self.tags[i].nom+"-----------------\n\n"
      if isinstance(self[i],list):
        for j in self[i]:
          s+=" • "+j+"\n\n"
      else:
        s+=self[i]+"\n\n"
      
    self.save(path+"/"+self.pdf.name+".txt",s)

  #Caractères à échapper dans un document xml
  XMLechap={"&":"&amp;",
           '"':"&quot;",
           "'":"&apos;",
           "<":"&lt;",
           ">":"&gt;"
           }
  #Échappement d'un document xml
  def echape(self,s):
    for cha in self.XMLechap:
      s=s.replace(cha,self.XMLechap[cha])
    return s

  #Fonction récursive de création des balises xml
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
        s+=self.echape(self[l[0]])
      elif type(l[1])==str:
        s+=self.echape(l[1])
      else:
        s+=self.balise(l[1])
      s+=t.baliseFin
    return s
  #Exportation au format xml
  def saveAsXml(self,path):
    #Syntaxe du document xml à produire
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

  #Fonction de création d'un fichier
  def save(self,path,valeur):
    file = open (path, 'w', encoding="utf8")
    file.write(valeur)
    file.close()


   
