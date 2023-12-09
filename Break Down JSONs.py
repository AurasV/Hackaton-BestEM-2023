import json
import os

# Step 1: Read the large JSON file
with open('unique_with_categories.json', 'r') as json_file:
    data = json.load(json_file)

# Step 2: Extract unique categories
unique_categories = set(item['Category'] for item in data)

# Step 3: Create a folder to store the separate JSON files
folder_name = 'JSONs Based on Categories'

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Step 4: Define the fields to remove
fields_to_remove = ["Country", "Customer ID", "Price", "Date", "Quantity", "Invoice", "Category"]

# Step 5: Iterate through the data, remove specified fields, and create separate JSON files for each category
for category in unique_categories:
    category_data = []
    for item in data:
        if item['Category'] == category:
            # Create a new item without the specified fields
            new_item = {key: value for key, value in item.items() if key not in fields_to_remove}
            category_data.append(new_item)

    filename = os.path.join(folder_name, f'{category}.json')

    with open(filename, 'w') as category_file:
        json.dump(category_data, category_file, indent=4)
