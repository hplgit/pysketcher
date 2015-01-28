#!/bin/sh

# Run spellcheck
doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Abort due to misspellings."
  exit 1
fi

main=main_sketcher
doconce format html $main

cp .ptex2tex.cfg-minted .ptex2tex.cfg
doconce format pdflatex $main --skip_inline_comments
ptex2tex -DMINTED $main
pdflatex -shell-escape $main
makeindex $main
pdflatex -shell-escape $main
pdflatex -shell-escape $main

doconce format sphinx $main --skip_inline_comments
doconce sphinx_dir author="H. P. Langtangen" version=0.1 theme=pyramid $main
python automake_sphinx.py

dest=../../pub/tutorial
cp ${main}.pdf $dest/pysketcher.pdf
#cp $main.html ../../tutorial/pysketcher.html
rm -rf $dest/html
cp -r sphinx-rootdir/_build/html $dest/html
