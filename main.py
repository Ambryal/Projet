#-----------------Modules distribués-----------------
#lel
import sys
from time import sleep
import glob, os
import shutil
from datetime import datetime


#-----------------Modules du projet-----------------

sys.path.insert(1, 'Modules')
import reader
from pdf import Pdf
from text import Text


#-----------------Données statiques-----------------

CURRENT_PDF_DIRECTORY = "PDF/Corpus_2021"


#-----------------Variables globales-----------------

#Liste des pdf à traduire
PDF=[Pdf(file) for file in glob.glob(CURRENT_PDF_DIRECTORY+"/*.pdf")]

#Traducteur de pdf
READER=reader.Reader()

#-----------------Outils-----------------

#timestamp
def now():
    return datetime.now().timestamp()


#-----------------Fonctions Principales-----------------

#Test d'efficacité des modules de convertissement
def test_converters_speed(path):
    for converter in READER.converters:
        time = now()
        name = converter.__name__
        print("CONVERTING WITH : "+name)
        folder = path+"/"+name
        try:
            shutil.rmtree(folder)
        except:
            pass
        os.mkdir(folder)
        for file in PDF:
            converter(file).save(folder+"/"+file.name+".txt")
        print("Total time : ",int(now()-time),"s\n")


#-----------------Fonctions de Display-----------------




#-----------------Exécution-----------------

#test_converters_speed("Artefacts/Sprint_1/Text_outputs_des_differents_modules")

def alone(s):
    for i in tx:
        if i.count(s)>0:
            return False
    return True
print(PDF[0].name)

tx=[c(PDF[0]).raw for c in READER.converters]

f=tx.pop()
s=""
l=[]

for i in f:
    s+=i
    if alone(s):
        l.append(s[:-1])
        s=i

print(l)
        






























