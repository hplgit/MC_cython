#!/bin/sh

python ~/hg/programs/spellcheck.py -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Misspellings!"  # use mydict.txt~.all~ as new dictionary.txt?
  exit 1
fi

doconce format latex MC_cython -DPRIMER_BOOK -DHEADER
doconce replace figs-MC_cython figs MC_cython.p.tex
