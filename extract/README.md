# Introduction
This script can be utilized to extract values from multiple timestamp rasters for time series analysis. In this script, ESRI shapefiles have been used as polygon boundaries to extract the values. These boundaries represent the extents of city boundaries for each year from 2000 to 2019.
# Change raster file name
1. Rename raster file as "ODIAC_CO2_1km_2000_01_Jan", where 2000 is the year 01 month as integer and lastly month as in Jan, feb so on.
2. Change the input and the output folder and Run the script.
# Method
Extracting values from raster files using corresponding shapefiles based on the same year, we can follow these steps in Python:
1. Iterate over the range of years.
2. For the same year, load each of the four seasonal raster files.
3. Required spatial analysis library (like rasterio for raster operations and geopandas for shapefile operations) to extract values from the raster layers using the shapefile as a mask.
