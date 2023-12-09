import json

# Load the JSON data from file
file_path = 'transactions_with_categories.json'  # Replace with your JSON file path
with open(file_path, 'r') as file:
    data = json.load(file)

# Dynamically generate categories based on the 'Category' field in the data
category_counts = {}

# Count the items in each category
for item in data:
    category = item.get('Category')
    if category:
        category_counts[category] = category_counts.get(category, 0) + 1

# Print the count of items in each category
for category, count in category_counts.items():
    print(f"{category}: {count}")
