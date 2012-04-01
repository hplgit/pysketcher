#!/bin/sh

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

cp basics.p.tex pysketcher_basics.p.tex
cp implementation.p.tex pysketcher_impl.p.tex
cp exercises.p.tex pysketcher_ex.p.tex
