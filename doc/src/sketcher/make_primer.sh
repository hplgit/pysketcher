#!/bin/sh

doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Abort due to misspellings."
  exit 1
fi

doconce format latex basics -DPRIMER_BOOK
doconce format latex implementation -DPRIMER_BOOK
doconce format latex exercises -DPRIMER_BOOK
# fix \code{} in figure captions
doconce replace "Hierarchy of figure elements in an instance of class \code{Vehicle0" "Hierarchy of figure elements in an instance of class \codett{Vehicle0" implementation.p.tex

# Modify syntax in exercises
doconce subst '\\subsection\{' '\\begin{exercise}\n\\exerentry{' exercises.p.tex
doconce subst '\\noindent\nFilename: \\code\{(.+?)\}' 'Name of program file: \\code{\g<1>}.\n\\hfill $\\diamond$\n\\end{exercise}' exercises.p.tex

# Figure refs are wrong
doconce replace "figs-sketcher/" "figs/" *.p.tex
doconce replace "wheel_on_inclined_plane" "wheel_on_inclined_plane_cropped" *.p.tex

# Fix exercises
doconce subst '\\subsection\{' '\\begin{exercise}\n\\exerentry{' $file
doconce subst 'Filename: \\code\{(.+?)\}\.' 'Name of program file: \\code{\g<1>}.\n\\hfill $\\diamond$\n\\end{exercise}' exercises.p.tex

doconce replace Section Chapter *.p.tex

cp basics.p.tex pysketcher_basics.p.tex
cp implementation.p.tex pysketcher_impl.p.tex
cp exercises.p.tex pysketcher_ex.p.tex
