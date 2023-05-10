from bloc import Bloc
from random import shuffle

"""
Objet héritant de la classe Liste modélisant un PDF sous forme à la fois d'une
liste de Blocs et d'une liste de pages (elles-mêmes une liste de Blocs).

Il possède toutes les méthodes qui permettront d'interpréter ses éléments
comme des mails, une intro, etc...
"""

class Carnet(list):
  
  def __init__(self,pdf):
    #Lien vers le pdf source
    self.pdf=pdf
    #Pages
    self.pages=[]

    #Initialisation de listes utiles par la suite
    #Liste des polices
    self.fonts=[]
    #Prémisse : Liste des Blocs avant l'Abstract
    self.premisse=[]
    #Parties du Document (1.1, 1.2,2.1, etc...)
    self.parts=[]
    #Police du titre des chapitres
    self.policeTitre=""

    #Évaluation de la position du corps
    self.corpsMax=1000000
    self.corpsMin=-1
    #Fallback si les chapitres n'ont pas pu être détectés
    self.corpsMaxParts=1000000
    self.corpsMinParts=-1

    #Position des Blocs correspondant aux mails
    self.posMail=[]

    #Création des blocs par analyse de la sortie de pymupdf
    pdf = pdf.open()
    for page in pdf:
        self.addPage()
        bloc=Bloc()
        source=page.get_text()
        for group in page.get_text("dict")["blocks"]:
            if "lines" in group.keys():
                for span in group['lines']:
                    #Parcours des lignes du pdf et regroupement de celles-ci
                    #en un seul Bloc tant qu'elles ont la même Police
                    for lines in span['spans']:
                        font=str(lines['size'])+lines['font']
                        size=lines['size']
                        line=lines['text']
                        pos=lines["bbox"]
                        if line.upper()==line and line.lower()!=line:
                            font=font+"upper"
                            size+=0.1
                        if bloc.font==None:
                            bloc.font=font
                            bloc.size=size
                            bloc.pos=pos
                        if bloc.font!=font:
                            self.addBloc(bloc)
                            bloc=Bloc(font=font,size=size,pos=pos)
                        while source.startswith("\n"):
                            if bloc.text!="":
                                bloc.text+="\n"
                            source=source[1:]
                        if source.startswith(line):
                            bloc.text+=line
                            while bloc.text.startswith(" "):
                                bloc.text=bloc.text[1:]
                        else:
                            #Erreur presque impossible venant de pymupdf
                            print("Erreur de lecture :\n"+line+"\n"+source[:100])
                            sys.exit()
                        source=source[len(line):]
        self.addBloc(bloc)
    pdf.close()

#Ajout d'une page au carnet
  def addPage(self):
    self.pages.append([])

#Ajout d'un bloc au carnet
  def addBloc(self,bloc):
    #Contrôle de la Police
    if bloc.font not in self.fonts:
      self.fonts.append(bloc.font)
    bloc.font=self.fonts.index(bloc.font)+1
    bloc.text=correct(bloc.text)
    #Ajout à la dernière page
    self.pages[-1].append(bloc.fixe())
    #Ajout à l'objet
    self.append(bloc.fixe())
    
#Détection du Titre
  def getTitre(self):
    max,arg,n,titre=-1,0,0,""
    #Détection du bloc de police maximale dans les premiers blocs
    for j in range(len(self.pages)):
      for i, bloc in enumerate(self.pages[j]):
        n+=1
        if bloc.size>max and len(bloc)>1 and horizontal(bloc):
          max=bloc.size
          arg=n
          titre=bloc
      #Suppression du texte précédant le titre
      if n>40:
        while self[0].size!=max:
          self.pop(0)
          if len(self.pages[0])==0:
            while len(self.pages[0])==0:
              self.pages.pop(0)
            self.pages[0].pop(0)
            break
          self.pages[0].pop(0)
        #Renvoi du titre sans retour à la ligne
        return sansRetour(titre)

#Détection des mails
  def getMail(self):

    mails=[]

    #Les mails sont recherchés dans la prémisse puis dans le document entier
    for zone in [self.getPremisse(),self]:
      if len(mails)>0:
        break
        
      #Éléments techniques
      res={}
      lastBloc=""

      #Détection des polices contenant des "@"
      for i, bloc in enumerate(zone):
        if "@" in bloc:
          if bloc.font not in res:
            res[bloc.font]=[]
            for j,b in enumerate(zone):
              if b.font==bloc.font:
                res[bloc.font].append(j)
      #Détection de la bonne police parmi celles-ci
      for font in res:
        for i in res[font]:
          bloc=zone[i]
          for n,word in enumerate(sansRetour(bloc).split(" ")):
            if "@" in word:
              #Cas (nom1,nom2,nom3)@ubs.fr
              if word.startswith("@"):
                if n!=0:
                  lastBloc=" ".join(sansRetour(bloc).split(" ")[0:n])
                if lastBloc=="":
                  if i==0:
                    lastBloc="_"
                  else:
                    lastBloc=zone[i-1]
                x=lastBloc.split(",")
                for person in x:
                  #Types de parenthèses
                  for cha in "{}[]() ":
                    person=person.replace(cha,"")
                  if person=="":
                    person="_"
                  mails.append(person+word)
                  self.posMail.append(bloc.pos)
                  if i!=0:
                    zone[i-1]=zone[i-1].fixe()
              #Cas nom1,nom2,nom3@ubs.fr
              elif "," in word:
                fin="@"+word.split("@")[1]
                words=word.split("@")[0].split(",")
                for w in words:
                  mails.append(w+fin)
                  self.posMail.append(bloc.pos)
              else:
                mails.append(word)
                self.posMail.append(bloc.pos)
              #Suppression des mails dans le carnet
              zone[i].text=zone[i].text.replace(word,"")
          zone[i]=zone[i].fixe()
          lastBloc=zone[i]
        break
      
    return mails

  
#Détection des noms
  def getNom(self,mail):

    #Fallback si les mails n'ont pas été détectés
    if mail==[]:
      return mail

    #Les noms sont détéctés dans la prémisse
    premisse=self.getPremisse()
    
    #Éléments techniques
    fonts=[]
    res=[0,["" for _ in mail],["" for _ in mail],""]

    for i, bloc in enumerate(premisse):
      s=bloc.font
      #Évaluation de la police la plus adéquate pour représenter les noms
      if s not in fonts:
        fonts.append(s)
        l=[]
        for j, b in enumerate(premisse):
          if b.font==s:
              #Séparation des noms par "," ";" "\n" " and " " & &
              for k in b.replace(",","\n").replace(";","\n").replace(" & ","\n").replace(" and ","\n").split("\n"):
                while k.startswith(" "):
                  k=k[1:]
                while k.endswith(" "):
                  k=k[:-1]
                #Si le nom est entre 2 et 4 mots, il est candidat
                if 2<=len(k.split(" "))<=4:
                  l.append(k)
        #Heuristique permutant l'ordre des noms et évaluant leur pertinence
        for _ in range(int(1000/(max(1,len(l))**2))):
          self.findNom(mail,res,l,1,s)
          shuffle(l)

    #Suppression des noms dans le carnet
    for i, bloc in enumerate(premisse):
      if bloc.font==res[3]:
        for name in res[2]:
          premisse[i].text=premisse[i].text.replace(name,"")
        premisse[i]=premisse[i].fixe()

    #Renvoi des noms sans double espace
    return clean(res[2])

#Fonction récursive évaluant la pertinence d'une association noms-mails
  def findNom(self,mail,res,l,proba,size):
    if len(mail)==0 or len(l)<len(mail):
      return
    for i in range(len(l)):
      #Évaluation de la pertinence d'un nom
      res[1][len(res[1])-len(mail)]=l[i]
      new_proba=proba*similarite(l[i],mail[0])
      if len(mail)>1:
        #Récursivité
        self.findNom(mail[1:],res,l[i+1:],new_proba,size)
      else:
        #Fin de récursivité : évaluation de la pertinence globale
        if new_proba>res[0]:
          res[0]=new_proba
          res[3]=size
          for i in range(len(res[1])):
            res[2][i]=res[1][i]

  
#Détection des affiliations
  def getUniv(self,mail):

    #Fallback si les mails n'ont pas été détectés
    if mail==[]:
      return mail

    #Mots clefs caractérisant une affiliation
    mots_clefs=["univ",
                "labo",
                "cole",
                "school",
                "nstitu",
                "epartmen",
                "épartemen"
                ]
    
    #Les affiliations sont détéctées dans la prémisse
    premisse=self.getPremisse()
    
    #Éléments techniques
    fonts=[]
    res=[]
    
    for i, bloc in enumerate(premisse):
      s=bloc.font
      if s not in fonts:
        fonts.append(s)
        l=[]
        for j, b in enumerate(premisse):
          if b.font==s:
              for k in b.split("\n"):
                #Détection des mots clefs
                for mc in mots_clefs:
                  if mc in k.lower():
                    l.append([k,b.pos])
                    streak=True
                    break
                else:
                  if len(l)>0 and streak:
                    l[-1][0]+="\n"+k
          else:
            streak=False
        if len(l)>len(res):
          res=l

    #Suppression des affiliations dans le carnet
    for i, bloc in enumerate(premisse):
      for adresse in res:
        for univ in adresse[0].split("\n"):
          premisse[i].text=premisse[i].text.replace(univ,"")
          premisse[i]=premisse[i].fixe()

    #Suppression des retours à la ligne
    for i in range(len(res)):
      res[i][0]=sansRetour(res[i][0])

    univ=["" for _ in mail]

    #Attribution des affiliations aux différents auteurs
    #Cas moins d'affiliations que d'auteur
    if 2*len(res)<=len(univ):#    if len(res)<len(univ):
      for i in range(len(univ)):
        for j in res:
          univ[i]+=" "+j[0]
    #Cas autant ou plus d'affiliations que d'auteur
    else:
      #Tentative d'attribuer les affiliations en fonction de la position des blocs
      if len(set([plus_pres(i[1],self.posMail) for i in res]))>1:
        for i in res:
          univ[plus_pres(i[1],self.posMail)]+=" "+i[0]
      else:
        #Fallback
        for i,r in enumerate(res):
          univ[i%len(univ)]+=" "+r[0]
    for i in range(len(univ)):
      if len(res)>0:
        if univ[i]=="":
          univ[i]=res[plus_pres(self.posMail[i],[j[1] for j in res])][0]
        else:
          univ[i]=univ[i][1:]
    
    return clean(univ)



#Détection des chapitres de l'article
  def getParts(self):
    #Type de numérotations
    langues=[["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"],
             ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]]

    #Éléments techniques
    fonts=[]
    res=[0,0,"",[],0,0]
    lastLine=""
    lastBloc=""
        
    if len(self.parts)==0:
      for i, bloc in enumerate(self):
        f=bloc.font
        #Détection de la police des titres
        if f not in fonts:
          lastLine=lastBloc
          fonts.append(f)
          for k, l in enumerate(langues):
            c=0
            r=[]
            #Valeurs permettant d'établir la pertinence de la police
            long=[0,0,0,0]
            for j, b in enumerate(self):
              long[0]+=len(b)
              if b.font==f:
                if c>len(l)-1:
                  long=[0,0,0,0]
                  break
                rattrapage=lastLine!="" and lastLine.font!=bloc.font and (lastLine.split("\n")[-1].endswith(l[c]) or lastLine.split("\n")[-1].startswith(l[c]))
                if b.startswith(l[c]) or rattrapage:
                  c+=1
                  long[1]+=long[2]
                  long[2]=0
                  r.append([b,""])
                  #Fallback si le numéro est dans la dernière ligne du bloc précedent
                  if rattrapage:
                    r[-1][0]=lastLine.split("\n")[-1]+r[-1][0]
                    long[3]+=len(r[-1][0])
                else:
                  #Extraction du titre du chapitre
                  if len(r)>0:
                    if r[-1][1]=="" and len(r[-1][0])<200:
                        r[-1][0]+=" "+b
                        long[3]+=len(b)
                    else:
                      r[-1][1]+=" "+b
                      long[2]+=len(b)
              elif len(r)>0:
                if r[-1][0]==str(l[c-1]):
                  r[-1][0]+=" "+b
                  long[3]+=len(b)
                else:
                  r[-1][1]+="\n"+b
                  long[2]+=len(b)
              if b=="\n" or b=="":
                lastLine=""
              else:
                lastLine=b
            #Évaluation de la pertinence de la police
            if long[1]>0 and long[0]/long[1]<2 and (res[4]=='' or (float(bloc.size)>float(res[4]))) and c>1:#c>res[0]:
              res=[c,k,f,r,bloc.size,long[3]/max(1,len(r))]
        lastBloc=bloc
      self.policeTitre=res[2]
      self.parts=res[3][:-1]
      if False:
        #sys.exit()
        for i in self.parts:
          print("_____________________")
          print(i[0])
          print("_____________________")
          print("---------------------")
          print(i[1])
          print("---------------------")

    return self.parts
  
#Détection d'une partie du document par mots clefs
  def findPart(self,l,reverse=False,fallback=True):

    #Recherche exacte dans le cas où findPartReverse est utilisé
    exact=None
    if reverse:
      exact=self.findPartReverse(l,fallback)
      
    #Recherche dans les chapitres
    for i, part in enumerate(self.getParts()):
      #Détection des mots clefs
      for keyword in l:
        if exact==part[0] or (not reverse and keyword in part[0].lower()):
          if reverse:
            self.corpsMaxParts=min(self.corpsMaxParts,i)
          else:
            self.corpsMinParts=max(self.corpsMinParts,i)
          return part[1][1:]
        
    flag=False
    res=""
    #Fallback si la partie n'était pas dans les chapitres
    for i, part in enumerate(self):
      if flag:
        #Reverse : on prend tout jusqu'à la fin du document
        if reverse:
          for _ in range(len(self)-i):
            res=self.pop()+res
          self.pop()
          return res
        #Extraction de la partie
        if (part.font==self.policeTitre and len(res)>100) or (self.policeTitre=="" and len(res)>1000):
          return res
        res+=part
        if i==len(self)-1:
          return res
      #Détection des mots clefs
      for keyword in l:
        if exact==part or (not reverse and keyword in part.lower()):
          if reverse:
            self.corpsMax=min(self.corpsMax,i)
          else:
            self.corpsMin=max(self.corpsMin,i)
          flag=True
          
    #Echec
    return "N/A"
  
#Méthode semblable à findPart mais recherchant depuis la fin du document
  def findPartReverse(self,l,fallback):

    res=""
    
    #Recherche dans les chapitres
    for part in reversed(self.getParts()):
      #Détection des mots clefs
      for keyword in l:
        flag=False
        if keyword in part[0].lower():
          res=part[0]
          flag=True
          break
      #Gestion des cas où la partie est en plusieurs chapitres successifs
      if not flag and res!="":
        break

    #Renvoi du titre exact de chapitre à chercher pour findPart
    if res!="":
      return res
      

    #Recherche dans les éléments ayant la police des chapitres
    #Puis dans tous les éléments pouvant être assimilés à un titre
    for tour in range(2):
      for i,part in enumerate(reversed(self)):
        if tour==1 or part.font==self.policeTitre:
          #Cas où la détection de la partie est jugée secondaire
          if not fallback and i>40:
            break
          #Détection des mots clefs
          for keyword in l:
            firstLine=part.lower().split("\n")
            firstLine.append("")
            firstLine=firstLine[0]
            if (isShort(part) and (keyword in part.lower())) or (len(firstLine)<15 and keyword in firstLine.lower()):
              #Renvoi du titre exact de chapitre à chercher pour findPart
              return part
    
    #Echec
    return "N/A"


#Détection de l'Abstract
  def getAbstract(self):
    return self.findPart(["bstract","b s t r a c t"])
  
#Détection de l'Introduction
  def getIntro(self):
    return self.findPart(["ntro"])

#Détection de la Discussion
  def getDiscu(self):
    return self.findPart(["iscussion"],True,False)

#Détection des Acknowlegements
  def getAknow(self):
    return self.findPart(["cknowledgement","cknowledgment"],True,False)

#Détection de la Conclusion
  def getConclu(self):
    return self.findPart(["onclusion"],True)

#Détection de la Bibliographie
  def getBiblio(self):
    return self.findPart(["eference","bliogr"],True)

#Détection de l'Abstract
  def getCorps(self):
    s=""
    #Détection du corps via les chapitres
    if self.corpsMinParts!=-1:
      for i in range(max(0,self.corpsMinParts+1),min(self.corpsMaxParts,len(self.getParts()))):
        s+="\n"+self.getParts()[i][0]+self.getParts()[i][1]
      return s[1:]
    else:
      #Fallback si les chapitres n'ont pas pû être détectés
      for i in range(max(0,self.corpsMin),min(self.corpsMax,len(self))):
        s+="\n"+self[i]
      return s[1:]

#Détection de la prémisse
  def getPremisse(self):
    if len(self.premisse)==0:
      mailFound=False
      #Parcours du carnet
      for bloc in self:
        #Renvoi si des mails ont été détectés et que le bloc est un paragraphe
        if isLong(bloc) and mailFound:
          break
        if "@" in bloc:
          mailFound=True
        self.premisse.append(bloc)
    return self.premisse

#Suppression du premier élément du carnet
  def shift(self):
    while len(self.pages[0])==0:
      self.pages.pop(0)
    self.pages[0].pop(0)
    return self.pop(0)

#Affichage
  def print(self, page=None, bloc=None):
    if page==None:
      l=self
    else:
      l=sum(self.pages[:page],[])
    if bloc!=None:
      l=l[:bloc]
      
    for i in l:
      print(i.print())

#Évaluation de la distance physique entre deux éléments
def plus_pres(p,l):
  r=[0,100000000]
  for i,q in enumerate(l):
    distance=(((p[2]+p[0])/2)-((q[2]+q[0])/2))**2+(((p[3]+p[1])/2)-((q[3]+q[1])/2))**2
    if distance<r[1]:
      r=[i,distance]
  return r[0]

#Évaluation de la distance syntaxique entre deux éléments
def similarite(a,b):
  if a=="" or a==" ":
    return 0
  n=[0,0]
  for i in b.split("@")[0]:
    w=i.lower()
    for j in a.split(" "):
      s=j.lower()
      while len(s)>0 and len(w)>0:
        if s[0]==w[0]:
          w=w[1:]
          n[1]+=1
        n[0]+=1
        s=s[1:]
  return n[1]/n[0]

#Suppression des double espaces
def clean(l):
  for i in range(len(l)):
    while "  " in l[i]:
      l[i]=l[i].replace("  "," ")
  return l

#Correction des caractères accentués
def correct(s):
  accents=[ ["e","`","è"],
            ["e","´","é"],
            ["e","́","é"],
            ["e","^","ê"],
            ["e","ˆ","ê"],
            ["e","¨","ë"],

            ["a","`","à"],
            ["a","´","á"],
            ["a","́","á"],
            ["a","^","â"],
            ["a","ˆ","â"],
            ["a","¨","ä"],

            ["i","`","ì"],
            ["i","´","í"],
            ["i","́","í"],
            ["i","^","î"],
            ["i","ˆ","î"],
            ["i","¨","ï"],

            ["o","`","ò"],
            ["o","´","ó"],
            ["o","́","ó"],
            ["o","^","ô"],
            ["o","ˆ","ô"],
            ["o","¨","ö"],

            ["u","`","ù"],
            ["u","´","ú"],
            ["u","́","ú"],
            ["u","^","û"],
            ["u","ˆ","û"],
            ["u","¨","ü"],
            ]
  for i in accents:
    s=s.replace(i[1]+i[0],i[2])
    s=s.replace(i[1]+i[0].upper(),i[2].upper())

  for i in accents:
    s=s.replace(i[0]+i[1],i[2])
    s=s.replace(i[0].upper()+i[1],i[2].upper())

  return s

#Caractérisation d'un bloc horizontal
def horizontal(b):
  return b.pos[2]-b.pos[0]>b.pos[3]-b.pos[1]

#Caractérisation d'un bloc court
def isShort(s):
  return s.count("\n")<2

#Caractérisation d'un bloc long
def isLong(s):
  return s.count("\n")>5 and len(s)>500

#Suppression des retours à la ligne
def sansRetour(s):
  return s.replace("\n"," ")

