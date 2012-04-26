#!/bin/sh

python ~/hg/programs/spellcheck.py -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then
  echo "Misspellings!"  # use mydict.txt~.all~ as new dictionary.txt?
  exit 1
fi

main=MC_cython

rm -rf sphinx-rootdir
doconce sphinx_dir author="H. P. Langtangen" title="Speeding Up Python Implementations of Monte Carlo Simulation" version=0.9 theme=pyramid $main
python automake-sphinx.py

doconce format pdflatex $main
ptex2tex -DMINTED $main
pdflatex -shell-escape $main
makeindex $main
pdflatex -shell-escape $main
pdflatex -shell-escape $main
