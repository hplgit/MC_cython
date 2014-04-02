#!/bin/sh
# prepare the document to part of a book (A Primer on Scientific
# Programming with Python)

doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Misspellings!"  # use mydict.txt~.all~ as new dictionary.txt?
  exit 1
fi

doconce format latex MC_cython -DPRIMER_BOOK
doconce replace fig-MC_cython figs MC_cython.p.tex
