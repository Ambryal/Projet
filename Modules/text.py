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

  def saveSprint2(self,path,file):
    s="Nom du Fichier :\n\n"+file
    r=self.raw.split("\n")
    i=0
    while r[i]=="" or "Aspose" in r[i] or r[i]=='\ufeff':
      i+=1

    s+="\n\nTitre:\n\n"+r[i]+"\n\nAuteurs :\n\n"
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
      i+=1

    
    
    file = open (path+"/"+file+".txt", 'w', encoding="utf8")
    file.write(s)
    print(s)
