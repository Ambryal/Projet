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

CURRENT_PDF_DIRECTORY = "res/tests/Corpus_2021/PDF"


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

#Fonction répondant au Sprint2
#Elle est assez bricolée et n'est ici que pour être fonctionelle
#Le projet sera refondu complètement
def sprint2(path):
    try:
        shutil.rmtree(path)
    except:
        pass
    os.mkdir(path)
    print(PDF)
    for file in PDF:
        READER.AW(file).saveSprint2(path,file.name)
        


#-----------------Fonctions de Display-----------------




#-----------------Exécution-----------------

#test_converters_speed("Artefacts/Sprint_1/Text_outputs_des_differents_modules")

sprint2("Artefacts/Sprint_2/titre_auteurs_abstract")
        






























