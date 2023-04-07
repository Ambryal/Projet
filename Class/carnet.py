from bloc import Bloc
from random import shuffle

class Carnet(list):
  
  def __init__(self,pdf):
    self.pdf=pdf
    self.pages=[]
    
    self.fonts=[]
    self.premisse=[]
    self.parts=[]

    self.policeTitre=""
    
    self.corpsMax=1000000
    self.corpsMin=-1
    self.corpsMaxParts=1000000
    self.corpsMinParts=-1

    self.posMail=[]
    
    pdf = pdf.open()
    for page in pdf:
        self.addPage()
        bloc=Bloc()
        source=page.get_text()
        for group in page.get_text("dict")["blocks"]:
            if "lines" in group.keys():
                for span in group['lines']:
                    for lines in span['spans']:
                        font=str(lines['size'])+lines['font']
                        size=lines['size']
                        line=lines['text']
                        #pos=((lines['bbox'][0]+lines['bbox'][2])/2,(lines['bbox'][1]+lines['bbox'][3])/2)
                        pos=lines["origin"]
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
                            print("Erreur de lecture :\n"+line+"\n"+source[:100])
                            sys.exit()
                        source=source[len(line):]
        self.addBloc(bloc)
    pdf.close()
    
  def addPage(self):
    self.pages.append([])

    
  def addBloc(self,bloc):
    if bloc.font not in self.fonts:
      self.fonts.append(bloc.font)
    bloc.font=self.fonts.index(bloc.font)+1
    bloc.text=correct(bloc.text)
    self.pages[-1].append(bloc.fixe())
    self.append(bloc.fixe())

#SUPPOSÉ : Le titre est toujours la suite d'éléments de la police la plus grande.
  def getTitre(self):
    max,n=-1,0
    for j in range(len(self.pages)):
      for i, bloc in enumerate(self.pages[j]):
        n+=1
        if bloc.size>max and len(bloc)>1:
          max=bloc.size
      if n>40:
        while self[0].size!=max:
          self.pop(0)
          while len(self.pages[0])==0:
            self.pages.pop(0)
          self.pages[0].pop(0)
        return sansRetour(self[0])
    
#SUPPOSÉ : Le mail est toujours dans la premisse
#          Les mails sont toujours dans la même police
#          Le mail est l'ensemble des éléments contenant "@" dans la police du 1er élément contenant "@".
#FALLBACK (retour vide) : Remplacer *Q*.* par *@*.* et recommencer.

  def getMail(self):

    mails=[]
    
    premisse=self.getPremisse()
    res={}

    lastBloc=""
    
    for i, bloc in enumerate(premisse):
      if "@" in bloc:
        if bloc.font not in res:
          res[bloc.font]=[]
          for j,b in enumerate(premisse):
            if b.font==bloc.font:
              res[bloc.font].append(j)
    for font in res:
      for i in res[font]:
        bloc=premisse[i]
        for n,word in enumerate(sansRetour(bloc).split(" ")):
          if "@" in word:
            if word.startswith("@"):
              if n!=0:
                lastBloc=" ".join(sansRetour(bloc).split(" ")[0:n])
              if lastBloc=="":
                if i==0:
                  lastBloc="_"
                else:
                  lastBloc=premisse[i-1]
              x=lastBloc.split(",")
              for person in x:
                for cha in "{}[]() ":
                  person=person.replace(cha,"")
                if person=="":
                  person="_"
                mails.append(person+word)
                self.posMail.append(bloc.pos)
                if i!=0:
                  premisse[i-1]=premisse[i-1].fixe()
            else:
              mails.append(word)
              self.posMail.append(bloc.pos)
            premisse[i].text=premisse[i].text.replace(word,"")
        premisse[i]=premisse[i].fixe()
        lastBloc=premisse[i]
      break
      
    return mails

  
#SUPPOSÉ : Les noms sont toujours dans la premisse
#          Il y a autant de noms que de mails
#          Ils sont dans le même ordre
#          Un nom est écrit sur une ligne
#          Les noms sont toujours dans la même police
  def getNom(self,mail):
    
    if mail==[]:
      return mail

    premisse=self.getPremisse()
    fonts=[]
    res=[0,["" for _ in mail],["" for _ in mail],""]
    for i, bloc in enumerate(premisse):
      s=bloc.font
      if s not in fonts:
        fonts.append(s)
        l=[]
        for j, b in enumerate(premisse):
          if b.font==s:
              for k in b.replace(",","\n").replace(";","\n").split("\n"):
                while k.startswith(" "):
                  k=k[1:]
                while k.endswith(" "):
                  k=k[:-1]
                if 2<=len(k.split(" "))<=4:
                  l.append(k)
        for _ in range(int(1000/(max(1,len(l))**2))):
          self.findNom(mail,res,l,1,s)
          shuffle(l)
        
    for i, bloc in enumerate(premisse):
      if bloc.font==res[3]:
        for name in res[2]:
          premisse[i].text=premisse[i].text.replace(name,"")
        premisse[i]=premisse[i].fixe()
        
    return clean(res[2])

  def findNom(self,mail,res,l,proba,size):
    if len(mail)==0 or len(l)<len(mail):
      return
    for i in range(len(l)):
      res[1][len(res[1])-len(mail)]=l[i]
      new_proba=proba*similarite(l[i],mail[0])
      if len(mail)>1:
        self.findNom(mail[1:],res,l[i+1:],new_proba,size)
      else:
        if new_proba>res[0]:
          res[0]=new_proba
          res[3]=size
          for i in range(len(res[1])):
            res[2][i]=res[1][i]

  
#SUPPOSÉ : Les affiliations sont toujours dans la premisse
#          Il y a autant d'affiliations que de mails
#          Elles sont dans le même ordre
#          Les affiliations sont toujours dans la même police
  def getUniv(self,mail):

    if mail==[]:
      return mail

    mots_clefs=["univ",
                "labo",
                "cole",
                "school",
                "nstitu",
                ]
    
    premisse=self.getPremisse()
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
          
    for i, bloc in enumerate(premisse):
      for adresse in res:
        for univ in adresse[0].split("\n"):
          premisse[i].text=premisse[i].text.replace(univ,"")
          premisse[i]=premisse[i].fixe()

    for i in range(len(res)):
      res[i][0]=sansRetour(res[i][0])

    univ=["" for _ in mail]

    for i in res:
      univ[plus_pres(i[1],self.posMail)]+="\n"+i[0]

    for i in range(len(univ)):
      if univ[i]=="":
        univ[i]=res[plus_pres(self.posMail[i],[j[1] for j in res])][0]
      else:
        univ[i]=univ[i][1:]
    
    return clean(univ)



#SUPPOSÉ : Les parties ont des titres numérotés, tous de la même police
  def getParts(self):
    langues=[["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20"],
             ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]]

    fonts=[]
    res=[0,0,"",[],0,0]
    lastLine=""
    lastBloc=""
        
    if len(self.parts)==0:
      for i, bloc in enumerate(self):
        f=bloc.font
        if f not in fonts:
          lastLine=lastBloc
          fonts.append(f)
          for k, l in enumerate(langues):
            c=0
            r=[]
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
                  if rattrapage:
                    r[-1][0]=lastLine.split("\n")[-1]+r[-1][0]
                    long[3]+=len(r[-1][0])
                else:
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
            if long[1]>0 and long[0]/long[1]<2 and (res[4]=='' or (float(bloc.size)>float(res[4]))) and c>1:#c>res[0]:
              res=[c,k,f,r,bloc.size,long[3]/max(0,len(r))]
        lastBloc=bloc
      self.policeTitre=res[2]
      self.parts=res[3][:-1]

    return self.parts

  def findPart(self,l,reverse=False,dontStop=False):

    exact=None
    if reverse:
      exact=self.findPartReverse(l)
    
    for i, part in enumerate(self.getParts()):
      for keyword in l:
        if exact==part[0] or (not reverse and keyword in part[0].lower()):
          if reverse:
            self.corpsMaxParts=min(self.corpsMaxParts,i)
          else:
            self.corpsMinParts=max(self.corpsMinParts,i)
          return part[1][1:]
    flag=False
    res=""
    for i, part in enumerate(self):
      if flag:
        if ((part.font==self.policeTitre and len(res)>100) or (self.policeTitre=="" and len(res)>1000)) and not dontStop:
          return res
        res+=part
        if i==len(self)-1:
          return res
      for keyword in l:
        if exact==part or (not reverse and keyword in part.lower()):
          if reverse:
            self.corpsMax=min(self.corpsMax,i)
          else:
            self.corpsMin=max(self.corpsMin,i)
          flag=True

    return "N/A"

  def findPartReverse(self,l):

    for part in reversed(self.getParts()):
      for keyword in l:
        if keyword in part[0].lower():
          return part[0]
        
    for tour in range(2):
      for part in reversed(self):
        if tour==1 or part.font==self.policeTitre:
          for keyword in l:
            firstLine=part.lower().split("\n")
            firstLine.append("")
            firstLine=firstLine[0]
            if (isShort(part) and (keyword in part.lower())) or (len(firstLine)<15 and keyword in firstLine.lower()):
              return part
    

    return "N/A"



  def getAbstract(self):
    return self.findPart(["bstract"])

  def getIntro(self):
    return self.findPart(["ntro"])

  def getDiscu(self):
    return self.findPart(["iscussion"],True)

  def getConclu(self):
    return self.findPart(["onclusion"],True)

  def getBiblio(self):
    return self.findPart(["eference","bliogr"],True,True)

  def getCorps(self):
    s=""
    if self.corpsMinParts!=-1:
      for i in range(max(0,self.corpsMinParts+1),min(self.corpsMaxParts,len(self.getParts()))):
        s+="\n"+self.getParts()[i][0]+self.getParts()[i][1]
      return s[1:]
    else:
      for i in range(max(0,self.corpsMin),min(self.corpsMax,len(self))):
        s+="\n"+self[i]
      return s[1:]
    
  def getPremisse(self):
    if len(self.premisse)==0:
      mailFound=False
      for bloc in self:
        if isLong(bloc) and mailFound:
          break
        if "@" in bloc:
          mailFound=True
        self.premisse.append(bloc)
    return self.premisse
        
  def shift(self):
    while len(self.pages[0])==0:
      self.pages.pop(0)
    self.pages[0].pop(0)
    return self.pop(0)
    
  def print(self, page=None, bloc=None):
    if page==None:
      l=self
    else:
      l=sum(self.pages[:page],[])
    if bloc!=None:
      l=l[:bloc]
      
    for i in l:
      print(i.print())


def plus_pres(p,l):
  r=[0,100000000]
  for i,q in enumerate(l):
    distance=(p[0]-q[0])**2+(p[1]-q[1])**2
    if distance<r[1]:
      r=[i,distance]
  return r[0]
  
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

def clean(l):
  for i in range(len(l)):
    while "  " in l[i]:
      l[i]=l[i].replace("  "," ")
  return l

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

def isShort(s):
  return s.count("\n")<2

def isLong(s):
  return s.count("\n")>5 and len(s)>500

def sansRetour(s):
  return s.replace("\n"," ")

