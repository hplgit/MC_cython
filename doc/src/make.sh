#!/bin/sh

# Note: The documentation is written in Doconce so the
# doconce program must be installed (code.google.com/p/doconce)

doconce spellcheck -d .dict4spell.txt *.do.txt
if [ $? -ne 0 ]; then exit 1; fi

main=main_MC_cython

rm -rf sphinx-rootdir
doconce sphinx_dir copyright="H. P. Langtangen" title="Speeding Up Python Implementations of Monte Carlo Simulation" version=0.9 theme=pyramid $main
python automake_sphinx.py

doconce format pdflatex $main
ptex2tex -DMINTED $main
pdflatex -shell-escape $main
makeindex $main
pdflatex -shell-escape $main
pdflatex -shell-escape $main

<<<<<<< HEAD
doconce format html $main --html-style=solarized
=======
doconce format html $main --html_style=solarized
>>>>>>> 7bd6a1553a1931ee41602034c7f291efefd9f0da
cp $main.html ${main}-solarized.html
doconce format html $main

# Copy to publish directory
dest=../web
rm -rf $dest/*.html $dest/*.pdf $dest/sphinx
cp -r fig-MC_cython $dest
cp -r ${main}-solarized.html $main.html $main.pdf sphinx-rootdir/_build/html $dest
cd $dest
mv html sphinx
