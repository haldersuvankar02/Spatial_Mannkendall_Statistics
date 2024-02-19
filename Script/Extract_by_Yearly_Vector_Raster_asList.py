# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 12:10:09 2024

@author: suvankarh
"""
import os
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import pandas as pd
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

def process_city_data(city, year, season_number, season_name):
    """Process data for a single city and return a DataFrame row."""
    rasterfile_path = os.path.join(raster_folder, f"{year}_{season_number}_{season_name}.tif")
    mean_raster_value = get_mean_raster_value_for_city(city, rasterfile_path)

    df_row = pd.DataFrame({
        'Year': [year],
        'Season': [season_name],
        'City Name': [city['Name']],
        'Mean CO2 Concentration': [mean_raster_value]
    })
    return df_row

def main():
    all_data = []
    
    for year in tqdm(range(2000, 2020), desc="Processing Years"):
        shapefile_path = os.path.join(shapefile_folder, f"{year}.shp")
        shapefile = gpd.read_file(shapefile_path)

        seasons = [("1", "Winter"), ("2", "Summer"), ("3", "Monsoon"), ("4", "Post-Mon")]
        for season_number, season_name in seasons:
            for _, city in shapefile.iterrows():
                city_data = process_city_data(city, year, season_number, season_name)
                all_data.append(city_data)

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv("E:\CO2_ODIAC\Seasonal\All_season\city_mean_co2_concentration.csv", index=False)
    print("Saved city_mean_co2_concentration.csv")

if __name__ == "__main__":
    main()
