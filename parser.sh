if [ -d venv ]
then
   venv/bin/python main.py $@
else
   echo "Installation en cours, veuillez patienter…"
   python -m venv venv
   venv/bin/pip install pdfminer-six
   venv/bin/pip install pypdf2
   venv/bin/pip install aspose-words
   venv/bin/pip install pypdf
   venv/bin/pip install pypdfium2
   venv/bin/python main.py $@
fi
