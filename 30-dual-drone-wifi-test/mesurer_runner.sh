#!/bin/bash

DATE=$(date +"%Y-%m-%d-%Hh-%Mm-%Ss")
FILENAME="./logs/experiment_log_""$DATE""_$1.txt"
touch $FILENAME

echo -e "\n\n [log] são $DATE \n\n"

python3 -u mesurer.py 2>&1 |& tee -a $FILENAME