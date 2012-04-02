#!/bin/sh

# Run spellcheck
python ~/hg/programs/spellcheck.py -d dictionary.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Misspellings!"  # use mydict.txt~.all~ as new dictionary.txt?
  exit 1
fi

main=wrap_sketcher
doconce format html $main

cp .ptex2tex.cfg-primer .ptex2tex.cfg
doconce format latex $main -DPRIMER_BOOK
ptex2tex $main
latex $main
makeindex $main
latex $main
latex $main
dvipdf $main
mv $main.pdf ${main}_primer.pdf

cp .ptex2tex.cfg-minted .ptex2tex.cfg
doconce format pdflatex $main
ptex2tex -DMINTED $main
pdflatex -shell-escape $main
makeindex $main
pdflatex -shell-escape $main
pdflatex -shell-escape $main

doconce format sphinx $main --skip_inline_comments
rm -rf sphinx-rootdir
doconce sphinx_dir author="H. P. Langtangen" version=0.1 theme=pyramid $main
python automake-sphinx.py

cp ${main}_primer.pdf ../../tutorial/pysketcher_blue.pdf
cp ${main}.pdf ../../tutorial/pysketcher.pdf
#cp $main.html ../../tutorial/pysketcher.html
cp -r sphinx-rootdir/_build/html ../../tutorial/html
