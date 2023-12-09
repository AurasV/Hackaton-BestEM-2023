import json
import os

# Step 1: Read the large JSON file
with open('unique_with_categories.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Create a folder to store the separate JSON files
folder_name = 'Cleaned JSON'

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Step 3: Define the fields to remove, including "Category"
fields_to_remove = ["Country", "Customer ID", "Price", "Date", "Quantity", "Invoice", "Category"]

# Step 4: Remove specified fields from all items
cleaned_data = []
for item in data:
    # Create a new item without the specified fields
    new_item = {key: value for key, value in item.items() if key not in fields_to_remove}
    cleaned_data.append(new_item)

# Step 5: Write the cleaned data to a JSON file
cleaned_filename = os.path.join(folder_name, 'Cleaned JSON.json')

with open(cleaned_filename, 'w') as cleaned_file:
    json.dump(cleaned_data, cleaned_file, indent=4)
