from time import sleep
#import pdftotext
import PyPDF2
import aspose.words as aw
from pypdf import PdfReader
import pypdfium2 as pdfium
from pdfminer.high_level import extract_text
import glob, os
from text import Text


#Traducteur
#Pend un objet de type Pdf
#Renvoie un objet de type Text

class Reader:
    
  def __init__(self):
    #liste des convertisseurs de pdf
    self.converters=[self.PYPDF,self.PYPDF2,self.AW,self.MINER,self.PDFIUM]
    
  #Text orientation : float / tuple de floats
  def PYPDF2(self,pdf,text_orientation = None):
        text = Text();
        reader = PyPDF2.PdfReader(pdf.path)
        for page in reader.pages:
            if text_orientation!=None:
                text.addPage(page.extract_text(text_orientation))
            else:
                text.addPage(page.extract_text())
        return text

  def PYPDF(self,pdf,text_orientation = None):
        text = Text();
        reader = PdfReader(pdf.path)
        for page in reader.pages:
            text.addPage(page.extract_text())
        return text

  def AW(self,pdf):
        text = Text();
        doc = aw.Document(pdf.path) 		
        doc.save("temp.txt")
        with open('temp.txt', encoding="utf8") as f:
            contents = f.read()
            text.raw = contents
        os.remove('temp.txt')
        return text
    
  def MINER(self,pdf):
        text = Text();
        text.raw = extract_text(pdf.path)
        return text

  def PDFIUM(self,pdf):
        text = Text();
        file = pdfium.PdfDocument(pdf.path)
        for page in file:
            textpage = page.get_textpage()
            text.addPage(textpage.get_text_range())
        return text























