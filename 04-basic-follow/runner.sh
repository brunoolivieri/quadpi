#!/bin/bash

#var=`date +"%FORMAT_STRING"`

now=`date +"%Y-%m-%d-%Hh-%Mmin"`
log_filename="./logs/${HOSTNAME}-${now}.log"
echo "Saving into ->" $log_filename

#echo $log_filename

nohup $1 >> $log_filename
tail -f $log_filename
