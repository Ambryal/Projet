#-----------------Modules distribués-----------------
import sys
from time import sleep
import glob, os
import shutil
from datetime import datetime

#-----------------Modules du projet-----------------

sys.path.insert(1, 'Class')
#Classe de gestion des sources Pdf
from pdf import Pdf
#Classe d'extraction d'un pdf en objet pratique de type liste
from carnet import Carnet
#Classe de transformation d'un carnet en objet pratique de type dictionnaire
#pouvant donner une sortie txt ou xml
from classeur import Classeur


#-----------------Données statiques-----------------

#Dossier source par défaut
CURRENT_PDF_DIRECTORY = "res/tests/Corpus TEST"#"res/tests/Corpus_2021/PDF"
#Dossier destination par défaut
DESTINATION_DIRECTORY = "Artefacts/Sprint_6/"
#Format de sortie par défaut
FORMAT = "xml"
#Sélection de fichier par défaut
SELECTION = None
#Survie de la fenetre après exécution par exécutable
STAY_ALIVE=True

#Gestion des arguments client
i=1
if len(sys.argv)>i and sys.argv[i].startswith("-"):
    if sys.argv[i]=="-t":
        FORMAT = "txt"
    if sys.argv[i]=="-x":
        FORMAT = "xml"
    i+=1
if len(sys.argv)>i and sys.argv[i]!="_":
    CURRENT_PDF_DIRECTORY=sys.argv[i]
i+=1
if len(sys.argv)>i and sys.argv[i]!="_":
    DESTINATION_DIRECTORY=sys.argv[i]
else:
    DESTINATION_DIRECTORY+=FORMAT


#-----------------Variables globales-----------------

#Liste des pdf à traduire
PDF=[Pdf(file) for file in glob.glob(CURRENT_PDF_DIRECTORY+"/*.pdf")]


#Affichage texte de choix des PDF à traduire
if len(PDF)!=0:
    print("PDF détectés :\n")
    for i in range(len(PDF)):
        print(i,PDF[i].name)
    print("Tapez le numéro ou le nom des PDF à traduire séparés d'espaces, ou ne tapez rien pour tout traduire.\n")
#Fallback si aucun PDF n'est trouvé
else:
    print("Aucun pdf détecté...")
    sleep(5)
    sys.exit()

#Sélection des fichiers à traduire
if SELECTION==None:
    SELECTION=input().lower()
    STAY_ALIVE=False

#Analyse de l'input client (choix par numéro, nom...)
for i in reversed(sorted([pdf.name.lower() for pdf in PDF], key=len)):
    SELECTION=SELECTION.replace(i,str([pdf.name.lower() for pdf in PDF].index(i)))
SELECTION=SELECTION.split(" ")

#-----------------Exécution-----------------

#Pour chaque PDF dans le dossier
for i, pdf in enumerate(PDF):
    #Si il est dans la sélection du client
    if str(i) in SELECTION or SELECTION==[""]:
        print("Extraction de "+pdf.name+"...")
        #Carnet(pdf).print(1,40)
        #sys.exit()
        carnet=Carnet(pdf)
        classeur=Classeur(carnet)
        if FORMAT=="txt":
            classeur.saveAsTxt(DESTINATION_DIRECTORY)
        else:
            classeur.saveAsXml(DESTINATION_DIRECTORY)


print("\nTerminé !")
if STAY_ALIVE:
    sleep(1000000)



























