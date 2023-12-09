import pandas as pd
import json

# Assuming json_data contains the list of JSON objects
json_file_path = 'sales and eodstocks.json'

with open(json_file_path, 'r') as file:
    json_data = json.load(file)
# Convert JSON data to a DataFrame
df = pd.DataFrame(json_data)

import numpy as np

# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract only the month from the date for grouping by month across all years
df['Month'] = df['Date'].dt.month

# Add a random extra value between 5 and 50 to each 'Sales' value
df['Sales_With_Extra'] = df['Sales'] + np.random.randint(5, 51, size=len(df))

# Calculate the median of modified sales for each Product_ID for each month (across all years)
median_sales_with_extra = df.groupby(['Product_ID', 'Month'])['Sales_With_Extra'].median()

# Convert the median sales data to a string for saving to a text file
median_sales_with_extra_str = median_sales_with_extra.to_string()

# Save the median sales data to a text file
median_sales_with_extra_file_path = 'monthly.txt'
with open(median_sales_with_extra_file_path, 'w') as file:
    file.write(median_sales_with_extra_str)

