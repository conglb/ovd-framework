#
#   CONFIGURATION
#

# imputing configuration, will be used in app_predcition.py
# To know which method is the most effective, you should run experiements on app_data_imputation.py
imputation = {
    "humidity"             :'Linear',
    "temperature"          :'Linear',
    "pressure"             :'Time Linear',
    "gust"                 :'Nearest',
    "windSpeed"            :"Time Linear",
    "windDir"              :"Time Linear",
    "windUCmp"             :"Time Linear",
    "windVCmp"             :"Time Linear",
    'power'                :"Linear",
    'humidity'             :"Time Linear", 
    'temperature'           :"Time Linear", 
    'waterTemperature'      :"Linear",
    'surfaceElevation'      :"Linear",
    'priWaveDir'            :"Linear",
    'priWavePeriod'         :'Linear',
    'waveSigH'              :'Linear',
    'windWavePeriod'        :'Linear',
    'windWaveDir'           :"Linear",
    'currentDir'            :"Time Linear",
    'currentSpeed'          :"Time Linear",
    'currentUCmp'           :"Time Linear",
    'currentVCmp'           :"Time Linear",
    'salinity'              :"Linear",
    'power service'        :"Nearest",
    'propeller speed service': "Nearest",
    'propeller speed'       :"Nearest"
}

standardized_columns = {
    'course'                :'sin', 
    'heading'               :'sin',              
    'pressure'              :'minmax', 
    'windDir'               :'cos',
    #'rot'                   :'minmax'
    'temperature'           :'minmax'
}