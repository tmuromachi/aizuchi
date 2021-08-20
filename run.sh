#!/bin/sh　-x

# ex) source run.sh

# echo -n "Please select Mode
# 0: Docker
# 1: venv
# input->"
# read mode

# echo -n "Please select the CUDA number:"
# read num

# activate venv
# source /home/tmuromachi/python/py37env/bin/activate

# git pull
# git pull

# run
# python main.py $1
# python main.py $num $mode

# if [ $mode = 1 ]; then
#   echo GOOGLE_APPLICATION_CREDENTIALS=./config/tmuromachi-ed1cc8e5a9ae.json
# fi

python ./src/google_stt.py