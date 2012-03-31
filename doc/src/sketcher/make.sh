#!/bin/sh

main=wrap_sketcher
doconce format html $main
exit 1

doconce format sphinx $main --skip_inline_comments
rm -rf sphinx-rootdir
doconce sphinx_dir author="H. P. Langtangen" version=0.1 theme=pyramid $main
python automake-sphinx.py

doconce format latex $main -DPRIMER_BOOK
ptex2tex -DMINTED $main
latex $main
makeindex $main
latex $main
latex $main
dvipdf $main
