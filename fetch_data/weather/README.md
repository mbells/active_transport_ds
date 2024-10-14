# Environment Canada weather data

See https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=48569

# Samples:

From "Station Inventory EN.csv":

    "Name","Province","Climate ID","Station ID","WMO ID","TC ID","Latitude (Decimal Degrees)","Longitude (Decimal Degrees)","Latitude","Longitude","Elevation (m)","First Year","Last Year","HLY First Year","HLY Last Year","DLY First Year","DLY Last Year","MLY First Year","MLY Last Year"
    "KITCHENER/WATERLOO","ONTARIO","6144239","48569","71368","YKF","43.46","-80.38","432739000","-802243000","321.6","2010","2024","2010","2024","2010","2024","",""

From daily data set:

    "Longitude (x)","Latitude (y)","Station Name","Climate ID","Date/Time","Year","Month","Day","Data Quality","Max Temp (°C)","Max Temp Flag","Min Temp (°C)","Min Temp Flag","Mean Temp (°C)","Mean Temp Flag","Heat Deg Days (°C)","Heat Deg Days Flag","Cool Deg Days (°C)","Cool Deg Days Flag","Total Rain (mm)","Total Rain Flag","Total Snow (cm)","Total Snow Flag","Total Precip (mm)","Total Precip Flag","Snow on Grnd (cm)","Snow on Grnd Flag","Dir of Max Gust (10s deg)","Dir of Max Gust Flag","Spd of Max Gust (km/h)","Spd of Max Gust Flag"
    "-80.38","43.46","KITCHENER/WATERLOO","6144239","2010-04-18","2010","04","18","","13.6","","2.5","","8.1","","9.9","","0.0","","","M","","M","0.0","","","","","M","43",""


# Legend

    A = Accumulated
    C = Precipitation occurred, amount uncertain
    E = Estimated
    F = Accumulated and estimated
    L = Precipitation may or may not have occurred
    M = Missing
    N = Temperature missing but known to be > 0
    S = More than one occurrence
    T = Trace
    Y = Temperature missing but known to be   < 0
    [empty] = Indicates an unobserved value
    ^ = The value displayed is based on incomplete data
    † = Data that is not subject to review by the National Climate Archives




Command line:
- year = change values in command line (`seq 1998 2008)
- month = change values in command line (`seq 1 12)
- format= [csv|xml]: the format output
- timeframe = 1: for hourly data
- timeframe = 2: for daily data
- timeframe = 3 for monthly data
- Day: the value of the "day" variable is not used and can be an arbitrary value
- For another station, change the value of the variable stationID
- For the data in XML format, change the value of the variable format to xml in the URL.

This data corresponds to three basic sampling frequencies of climate data collection:

    Hourly data is provided for each hour of the day requested
    Daily data is provided for each day of the month requested
    Monthly data is provided for each month of the year requested
