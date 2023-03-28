echo "Installation en cours, veuillez patienter…"
git clone https://github.com/Ambryal/Projet.git
cd Projet
python -m venv venv
venv/bin/pip install pymupdf
venv/bin/python main.py $@
