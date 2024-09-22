#!/bin/bash

# AIS Hub Data Aggregator
# https://github.com/ianrenton/aishub-data-aggregator

# Supply your own AIS Hub API username
USERNAME=AH_TRIAL_7EBC4392
TIME=`date '+%F_%H.%M.%S'`
FILE_NAME="./data/aishub.com/aishub-${TIME}.csv"

# Retrieve data
wget -q -O $FILE_NAME "http://data.aishub.net/ws.php?username=${USERNAME}&format=1&output=csv&compress=0" 
