#!/bin/sh

# Run spellcheck
doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Abort due to misspellings."
  exit 1
fi

name=main_sketcher
doconce format html $name

#cp .ptex2tex.cfg-minted .ptex2tex.cfg
doconce format pdflatex $name --skip_inline_comments --latex_code_style=pyg
#ptex2tex -DMINTED $name
pdflatex -shell-escape $name
makeindex $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name
cp $name.pdf pysketcher.pdf

html=pysketcher
doconce format html $name --skip_inline_comments --html_style=boostrap_bluegray --html_output=$html
doconce split_html ${html}.html

doconce format sphinx $name --skip_inline_comments
doconce sphinx_dir copyright="H. P. Langtangen" version=0.1 theme=pyramid $name
python automake_sphinx.py

# Publish
dest=../../pub/tutorial
name=pysketcher
cp ${name}.html ._${name}*.html ${name}.pdf $dest/
rm -rf $dest/html
cp -r sphinx-rootdir/_build/html $dest/html
