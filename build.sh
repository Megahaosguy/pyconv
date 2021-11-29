#!/bin/bash
echo "Buidling pyconv.py"
python3 -m nuitka --quiet --show-progress --remove-output ./pyconv.py
echo "Buidling hashvideo.py"
python3 -m nuitka --quiet --show-progress --remove-output ./hashvideo.py