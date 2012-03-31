#!/bin/sh

doconce format latex sketcher -DPRIMER_BOOK
# fix \code{} in figure captions
doconce replace "Hierarchy of figure elements in an instance of class \code{Vehicle0" "Hierarchy of figure elements in an instance of class \codett{Vehicle0" sketcher.p.tex

ptex2tex sketcher
