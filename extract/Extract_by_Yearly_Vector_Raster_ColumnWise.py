# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 14:47:27 2024

@author: suvankarh
"""
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import pandas as pd
import os
from tqdm import tqdm

# Define the folder paths here
shapefile_folder = "E:\CO2_ODIAC\DATA_backup\Boundary\WGS_New"
raster_folder = "E:\CO2_ODIAC\Seasonal\All_season\ODIAC_CO2_Seasonal"

def get_mean_raster_value_for_city(city_shape, rasterfile):
    """Calculates the mean value from a raster file for a given city shape."""
    with rasterio.open(rasterfile) as src:
        out_image, out_transform = mask(src, [city_shape.geometry], crop=True)
        masked_array = np.ma.masked_array(out_image, out_image == src.nodata)
        return masked_array.mean()

def main():
    # Prepare the DataFrame structure with Year and Season
    columns = ['Year', 'Season']
    seasons = [("1", "Winter"), ("2", "Summer"), ("3", "Monsoon"), ("4", "Post-Mon")]
    
    # Preparing data structure to hold the results
    result_data = {}

    for year in tqdm(range(2000, 2020), desc="Overall Progress"):
        shapefile_path = os.path.join(shapefile_folder, f"{year}.shp")
        shapefile = gpd.read_file(shapefile_path)

        # Add city names to columns if not already added
        for city_name in shapefile['Name']:
            if city_name not in columns:
                columns.append(city_name)

        for season_number, season_name in seasons:
            row_key = (year, season_name)
            if row_key not in result_data:
                result_data[row_key] = {'Year': year, 'Season': season_name}

            for _, city in shapefile.iterrows():
                rasterfile_path = os.path.join(raster_folder, f"{year}_{season_number}_{season_name}.tif")
                mean_raster_value = get_mean_raster_value_for_city(city, rasterfile_path)
                result_data[row_key][city['Name']] = mean_raster_value

    # Creating DataFrame from result_data
    final_df = pd.DataFrame.from_dict(result_data, orient='index', columns=columns)
    final_df.to_csv("E:\CO2_ODIAC\Seasonal\All_season\city_mean_co2_ColumnWise.csv", index=False)
    print("Saved city_mean_co2_ColumnWise.csv")

if __name__ == "__main__":
    main()
