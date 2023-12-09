import json
from datetime import datetime

# Path to your JSON file
json_file_path = 'sales and eodstocks.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Convert and format the 'Date' field in each JSON object
for item in json_data:
    # Convert epoch time (in milliseconds) to datetime object
    # Divide by 1000 to convert milliseconds to seconds
    date = datetime.utcfromtimestamp(item['Date'] / 1000)

    # Format the date in YYYY-MM-DD
    formatted_date = date.strftime('%Y-%m-%d')

    # Update the 'Date' field in the JSON object
    item['Date'] = formatted_date

# Save the updated JSON data back to the file
with open(json_file_path, 'w') as file:
    json.dump(json_data, file, indent=4)
