# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 15:33:53 2024

@author: suvankarh
"""
import pandas as pd
from tqdm import tqdm
import pymannkendall as mk

# Load your CSV file into a pandas DataFrame
file_path = 'E:\CO2_ODIAC\Seasonal\All_season\city_mean_co2_ColumnWise.csv'
outfol = 'E:\CO2_ODIAC\Seasonal\All_season'
df = pd.read_csv(file_path)

# Extract unique city names
cities = df.columns[2:]  # Assuming the first two columns are 'Year' and 'Season'

# Loop through each season
seasons = ['Winter', 'Summer', 'Monsoon', 'Post-Mon']

for season in seasons:
    # Filter data for the current season
    season_df = df[df['Season'] == season]

    # Create an empty DataFrame to store results for the current season
    result_df = pd.DataFrame(columns=['City', 'Trend', 'H', 'P', 'Z', 'Tau', 'S', 'Var_S', 'Slope',
                                      'Mean', 'SD', 'SEM', 'Min', 'Max'])
    
    # Initialize the progress bar
    progress_bar = tqdm(total=len(cities), desc=f'Mann-Kendall tests for {season}', position=0)

    # Loop through each city for the current season
    for city_name in cities:
        # Extract time and CO2 values for the current city and season
        time_series = season_df['Year']
        co2_values = season_df[city_name]

        # Perform Mann-Kendall test
        result = mk.original_test(co2_values, alpha = 0.05)

        # Calculate statistics
        mean = co2_values.mean()
        sd = co2_values.std()
        sem = sd / (len(co2_values) ** 0.5)
        min_value = co2_values.min()
        max_value = co2_values.max()

        # Append results and statistics to the DataFrame
        result_df = pd.concat([result_df, pd.DataFrame({
            'City': [city_name],
            'Trend': [result.trend],
            'H': [result.h],
            'P': [result.p],
            'Z': [result.z],
            'Tau': [result.Tau],
            'S': [result.s],
            'Var_S': [result.var_s],
            'Slope': [result.slope],
            'Mean': [mean],
            'SD': [sd],
            'SEM': [sem],
            'Min': [min_value],
            'Max': [max_value]
        })], ignore_index=True)
        
        # Update the progress bar
        progress_bar.update(1)
        
        # Close the progress bar
    progress_bar.close()

    # Save the results for the current season to a new CSV file
    result_file_path = outfol + f'\mann_kendall_results_{season}.csv'
    result_df.to_csv(result_file_path, index=False)

    print(f"Mann-Kendall tests for {season} completed, and results saved to {result_file_path}")
