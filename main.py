#-----------------Modules distribués-----------------
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
DESTINATION_DIRECTORY = "Artefacts/Sprint_3/"
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
  

#Fonction répondant au Sprint3
#Elle est assez bricolée et n'est ici que pour être fonctionelle
#Le projet sera refondu complètement
def sprint3(path,format):
    try:
        shutil.rmtree(path)
    except:
        pass
    os.mkdir(path)
    for file in PDF:
        print(file.name+"...")
        READER.AW(file).saveSprint3(path,file.name,format)
        #return
        
def test():
    for file in PDF:
        READER.MINER(file)
        return

#-----------------Fonctions de Display-----------------




#-----------------Exécution-----------------

#test_converters_speed("Artefacts/Sprint_1/Text_outputs_des_differents_modules")
#sprint3(DESTINATION_DIRECTORY,FORMAT)

import fitz
    
def shatter(pdf):
    print(pdf.path)
    fonts=[]
    results = []
    pdf = fitz.open(pdf.path)
    for page in pdf:
        results.append([])
        para={"text":""}
        s=page.get_text()
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block.keys():
                for span in block['lines']:
                    for lines in span['spans']:
                        f=str(lines['size'])+lines['font']
                        l=lines['text']
                        if f not in fonts:
                            fonts.append(f)
                        f=fonts.index(f)
                        if "font" not in para:
                            para["font"]=f
                            para["size"]=lines['size']
                        if para["font"]!=f:
                            results[-1].append(para)
                            para={"text":"","font":f,"size":lines['size']}
                        while s.startswith("\n"):
                            if para["text"]!="":
                                para["text"]+="\n"
                            s=s[1:]
                        if s.startswith(l):
                            para["text"]+=l
                            while para["text"].startswith(" "):
                                para["text"]=para["text"][1:]
                        else:
                            print("Erreur de lecture :\n"+l+"\n"+s[:100])
                            sys.exit()
                        s=s[len(l):]
        results[-1].append(para)
    pdf.close()
    for i in results[:1]:
        for j in i[:40]:
            print("----------------------------------","Police :",+j["font"],"        Taille : "+str(round(j["size"])))
            print(j["text"])
    sys.exit()
    return results

shatter(PDF[11])

for i in PDF:
    shatter(i)


#print(s,t)


#test()





























