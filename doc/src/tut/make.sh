#!/bin/bash

function system {
  "$@"
  if [ $? -ne 0 ]; then
    echo "make.sh: unsuccessful command $@"
    echo "abort!"
    exit 1
  fi
}

# Run spellcheck
system doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Abort due to misspellings."
  exit 1
fi

name=main_sketcher
system system doconce format html $name --html_output=${name}-draft

system doconce format pdflatex $name --skip_inline_comments --latex_code_style=pyg
system pdflatex -shell-escape $name
system makeindex $name
pdflatex -shell-escape $name
pdflatex -shell-escape $name
cp $name.pdf pysketcher.pdf

html=pysketcher
system doconce format html $name --skip_inline_comments --html_style=bootswatch_readable --html_output=$html
system doconce split_html ${html}.html --pagination

system doconce format sphinx $name --skip_inline_comments
system doconce sphinx_dir theme=alabaster $name
python automake_sphinx.py

# Publish
dest=../../pub/tutorial
name=pysketcher
cp ${name}.html ._${name}*.html ${name}.pdf $dest/
rm -rf $dest/html
cp -r sphinx-rootdir/_build/html $dest/html
cp -r fig-tut $dest
