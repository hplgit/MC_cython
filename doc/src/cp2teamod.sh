#!/bin/sh

sh make.sh
dest=~/vc/hplgit.github.com/teamods/MC_cython
cd ../web

cp -r fig-MC_cython $dest
cp -r *.html *.pdf sphinx $dest
