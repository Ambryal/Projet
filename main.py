#-----------------Modules distribués-----------------
import sys
from time import sleep
import glob, os
import shutil
from datetime import datetime


#-----------------Modules du projet-----------------

sys.path.insert(1, 'Class')
from pdf import Pdf
from carnet import Carnet
from classeur import Classeur


#-----------------Données statiques-----------------

CURRENT_PDF_DIRECTORY = "res/tests/Corpus_2021/PDF"
DESTINATION_DIRECTORY = "Artefacts/Sprint_4/"
FORMAT = "txt"

i=1
if len(sys.argv)>i and sys.argv[i].startswith("-"):
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

print("PDF détectés :_n\n")
for i in range(len(PDF)):
    print(i,PDF[i].name)
    
print("Tapez le numéro ou le nom des PDF à traduire séparés d'espaces, ou ne tapez rien pour tout traduire.")

SELECTION=input().lower()

for i in reversed(sorted([pdf.name.lower() for pdf in PDF], key=len)):
    SELECTION=SELECTION.replace(i,str([pdf.name.lower() for pdf in PDF].index(i)))

SELECTION=SELECTION.split(" ")

#-----------------Exécution-----------------


for i, pdf in enumerate(PDF):
    if str(i) in SELECTION or SELECTION==[""]:
        print("Extraction de "+pdf.name+"...")
        c=Classeur(Carnet(pdf))
        if FORMAT=="txt":
            c.saveAsTxt(DESTINATION_DIRECTORY)
        else:
            c.saveAsXml(DESTINATION_DIRECTORY)






























