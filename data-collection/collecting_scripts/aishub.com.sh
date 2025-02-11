#!/bin/bash

# Supply your own AIS Hub API username hier
USERNAME=AH_TRIAL_7EBC4392
TIME=`date '+%F_%H.%M.%S'`
FILE_NAME="../data/raw_files/aishub.com/aishub-${TIME}.csv"

# Retrieve data
wget -q -O $FILE_NAME "http://data.aishub.net/ws.php?username=${USERNAME}&format=1&output=csv&compress=0" 
echo $FILE_NAME