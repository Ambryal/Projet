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

