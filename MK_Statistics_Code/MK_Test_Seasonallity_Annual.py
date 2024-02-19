# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 18:10:28 2023

@author: suvankarh
"""

import pandas as pd
import pymannkendall as mk

# Load your CSV file into a pandas DataFrame
file_path = 'E:\CO2_ODIAC\Seasonal\All_season\city_mean_co2_ColumnWise.csv'
outfol = 'E:\CO2_ODIAC\Seasonal\All_season'
df = pd.read_csv(file_path)

cities = df.columns[2:]  # Assuming the first two columns are 'Year' and 'Season'

# Create an empty DataFrame to store results
result_df = pd.DataFrame(columns=['City', 'Trend', 'H', 'P', 'Z', 'Tau', 'S', 'Var_S', 'Slope',
                                  'Mean', 'SD', 'SEM', 'Min', 'Max'])

# Loop through each city
for city_name in cities:
    # Extract time and CO2 values for the current city
    time_series = df['Season']
    co2_values = df[city_name]

    # Perform Mann-Kendall test
    result = mk.seasonal_test(co2_values, period = 4, alpha = 0.05)
    
    # Calculate statistics
    mean = co2_values.mean()
    sd = co2_values.std()
    sem = sd / (len(co2_values) ** 0.5)
    min_value = co2_values.min()
    max_value = co2_values.max()

    # Append results to the DataFrame
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

# Save the results to a new CSV file
result_file_path = outfol + '\MK_Seasonality2.csv'
result_df.to_csv(result_file_path, index=False)

print("Mann-Kendall tests completed, and results saved to", result_file_path)