#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GIT_ROOT=$(cd ${SCRIPT_DIR}; git rev-parse --show-toplevel)

cd ${GIT_ROOT}/data

mkdir pedestrians_cyclists
cd pedestrians_cyclists

wget https://app2.kitchener.ca/appdocs/opendata/DBAdataSets/Trails_Counters_Pedestrians_Cyclists.csv

wget -O metadata1.json https://services1.arcgis.com/qAo1OsXi67t7XgmS/ArcGIS/rest/services/Active_Transportation_Eco_Counters/FeatureServer/1?f=json
