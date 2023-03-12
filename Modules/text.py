import os

#Objet représentant une traduction en format texte
class Text:
  def __init__(self):
    #texte brut
    self.raw = ""
    #texte paginé
    self.pages = []

  #Ajout d'une page au résultat
  def addPage(self,page):
    self.pages.append(page)
    self.raw+=page+"\n"

  def save(self, path):
    file = open (path, 'w', encoding="utf8")
    file.write(self.raw)

  def saveSprint3(self,path,file,format):
    s="Nom du Fichier :\n\n"+file
    r=self.raw.split("\n")
    i=0
    while r[i]=="" or "Aspose" in r[i] or r[i]=='\ufeff':
      i+=1

    s+="\n\nTitre :\n\n"+r[i]+"\n\nAuteurs :\n\n"
    i+=1

    if r[i]=="":
      i+=1
    n=0
    while (r[i]!="" or n==0) and not r[i].startswith("Abstract"):
      if r[i]!="" and "Aspose" not in r[i]:
        s+=r[i]
        n+=1
      i+=1
    s+="\n\nAbstract :\n\n"
    while i<len(r):
      if r[i].startswith("Abstract"):
        i+=1
        while r[i]!="":
          s+=r[i]
          i+=1
        break
      i+=1
      
    s+="\n\nBibliographie :\n\n"
    while i<len(r):
      if r[i].startswith("References"):
        i+=1
        while i<len(r):
          s+=r[i]
          i+=1
      i+=1
    s+="\n"
    
    #mails
    auteurs=s.split("\n\nAuteurs :\n\n")[1].split("\n\nAbstract :\n\n")[0]
    mots=auteurs.split(" ")
    mails=[]
    noms=[]
    for i in mots:
      if "@" in i:
        mails.append(i)
      else:
        noms.append(i)
    mails="\n".join(mails)
    noms=" ".join(noms)
    s=s.replace("\n\nAuteurs :\n\n"+auteurs+"\n\nAbstract :\n\n",
                "\n\nAuteurs :\n\n"+noms
                +"\n\nCourriels :\n\n"+mails
                +"\n\nAbstract :\n\n")

    #auteurs xml
    mails=mails.split("\n")
    noms=[noms]
    while len(mails)>len(noms):
      noms.append("")
    xml="\n<auteurs>"
    for i in range(len(mails)):
      xml+="\n<auteur>\n<name>"+noms[i]+"</name>"+"\n<mail>"+mails[i]+"</mail>"
    xml+="</auteurs>"
    
    if format=="xml":
      s="<article>"+"\n<preamble> "+s.split("Nom du Fichier :\n\n")[1].split("\n\nTitre :\n\n")[0]+" </preamble>"+"\n<titre> "+s.split("\n\nTitre :\n\n")[1].split("\n\nAuteurs :\n\n")[0]+" </titre>"+xml+"\n<abstract> "+s.split("\n\nAbstract :\n\n")[1].split("\n\nBibliographie :\n\n")[0]+" </abstract>"+"\n<biblio> "+s.split("\n\nBibliographie :\n\n")[1]+"</biblio>"+"</article>"
       

    file = open (path+"/"+file+"."+format, 'w', encoding="utf8")
    file.write(s)
    print(s)
