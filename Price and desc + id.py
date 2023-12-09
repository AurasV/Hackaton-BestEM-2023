import json

def filter_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    filtered_data = []

    for item in data:
        filtered_item = {
            "Product_ID": item.get("Product_ID", ""),
            "Description": item.get("Description", ""),
            "Price": item.get("Price", ""),
            "Category": item.get("Category", "")
        }
        filtered_data.append(filtered_item)

    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=2)

if __name__ == "__main__":
    input_file_path = "unique_with_categories.json"
    output_file_path = "unique_with_price_category_and_desc.json"

    filter_json(input_file_path, output_file_path)

    print(f"Filtered data saved to {output_file_path}")
