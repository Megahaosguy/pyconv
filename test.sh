#!/bin/sh
#echo "rm  ~/.haosoft/pyconv.cfg"
#rm  ~/.haosoft/pyconv.cfg
#echo "Initial Run (should work)"
#echo "./pyconv.py ex1.png"
./pyconv.py ex1.png
#echo "./pyconv.py ex2.jpg"
./pyconv.py ex2.jpg
#echo "./pyconv.py ex3.gif"
./pyconv.py ex3.gif
#echo "Second Run (should fail)"
#echo "./pyconv.py ex1.png"
./pyconv.py ex1.png
#echo "./pyconv.py ex2.jpg"
./pyconv.py ex2.jpg
#echo "./pyconv.py ex3.gif"
./pyconv.py ex3.gif
echo "rm BG*"
rm BG*
