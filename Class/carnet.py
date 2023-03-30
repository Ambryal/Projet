from bloc import Bloc

class Carnet(list):
  
  def __init__(self,pdf):
    self.pdf=pdf
    self.pages=[]
    self.fonts=[]

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
                        if bloc.font==None:
                            bloc.font=font
                            bloc.size=size
                        if bloc.font!=font:
                            self.addBloc(bloc)
                            bloc=Bloc(font=font,size=size)
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
    self.pages[-1].append(bloc.fixe())
    self.append(bloc.fixe())

  def getTitre(self):
    max=-1
    for i in range(len(self)):
      if self[i].size>max:
        max=self[i].size
    while self[0].size!=max:
      self.pop(0)
      while len(self.pages[0])==0:
        self.pages.pop(0)
      self.pages[0].pop(0)
    return sansRetour(self[0])
    

  def print(self, page=None, bloc=None):
    if page==None:
      l=self
    else:
      l=sum(self.pages[:page],[])
    if bloc!=None:
      l=l[:bloc]
      
    for i in l:
      print(i.print())

def sansRetour(s):
  return s.replace("\n"," ")

