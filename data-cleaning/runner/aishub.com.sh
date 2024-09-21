#!/bin/bash

# AIS Hub Data Aggregator
# https://github.com/ianrenton/aishub-data-aggregator

# Supply your own AIS Hub API username
USERNAME=AH_TRIAL_7EBC4392
TIME=`date '+%F_%H:%M:%S'`
FILE_NAME="aishub-${TIME}.csv"

# Retrieve data
wget -q "http://data.aishub.net/ws.php?username=${USERNAME}&format=1&output=csv&compress=0" -O $FILE_NAME

