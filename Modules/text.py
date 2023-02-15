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
    s=file
    r=self.raw.split("\n")
    i=0
    while r[i]=="" or "Aspose" in r[i]:
      i+=1

    s+="\n"+r[i]
    i+=1

    
    
    file = open (path+"/"+file+".txt", 'w', encoding="utf8")
    file.write(s)
    
    
