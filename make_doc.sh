#!/bin/sh

cd src-MC_cython
sh clean.sh
cd ..

tar cvzf MC_cython.tar.gz src-MC_cython
if [ ! -d _static ]; then
  mkdir _static
fi
mv MC_cython.tar.gz _static

doconce format sphinx MC_Cython.do.txt -DHEADER
if [ $? -ne 0 ]; then
  echo "Unsuccessful doconce format sphinx command"
  exit 1
fi
rm -rf sphinx-rootdir
doconce sphinx_dir author="Hans Petter Langtangen" title="Speeding Up Python Implementations of Monte Carlo Simulation" MC_Cython.do.txt
python automake-sphinx.py


