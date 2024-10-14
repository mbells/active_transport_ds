#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
GIT_ROOT=$(cd ${SCRIPT_DIR}; git rev-parse --show-toplevel)

cd ${GIT_ROOT}/data/weather


stationID=48569 # KITCHENER/WATERLOO, YKF, valid: 2010-2024

#for year in `seq 2010 2011`; do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${stationID}&Year=${year}&timeframe=3&submit=Download+Data" ;done

#https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=48569&Year=2019&timeframe=3&submit=Download+Data

#for year in `seq 2007 2008`;do for month in `seq 1 12`;do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=1706&Year=${year}&Month=${month}&Day=14&timeframe=3&submit= Download+Data" ;done;done


#for year in `seq 2007 2008`;do for month in `seq 1 1`;do wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${stationID}&Year=${year}&Month=${month}&Day=14&timeframe=2&submit=Download+Data" ;done;done

# Daily:
function fetch_daily {
    for year in `seq 2010 2024`;do
        wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${stationID}&Year=${year}&timeframe=2&submit=Download+Data"
    done
}

# Hourly:
function fetch_hourly {
    for year in `seq 2010 2024`;do
        for month in `seq 1 12`;do
            wget --content-disposition "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=${stationID}&Year=${year}&Month=${month}&timeframe=1&submit=Download+Data"
        done
    done
}

fetch_daily
fetch_hourly

