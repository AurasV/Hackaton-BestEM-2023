import json

def merge_json(product_json_file, description_json_file, output_file):
    with open(product_json_file, 'r') as f1, open(description_json_file, 'r') as f2:
        product_data = json.load(f1)
        description_data = json.load(f2)

    merged_data = []

    for product_entry in product_data:
        product_id = product_entry.get("Product_ID")
        description_entry = next((entry for entry in description_data if entry.get("Product_ID") == product_id), None)

        if description_entry:
            merged_entry = {**product_entry, "Description": description_entry.get("Description")}
            merged_data.append(merged_entry)

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)

if __name__ == "__main__":
    # Hardcoded file paths
    product_file_path = "monthly_sales.json"
    description_file_path = "unique desc and id.json"
    output_file_path = "monthly_sales_with_desc.json"

    merge_json(product_file_path, description_file_path, output_file_path)

    print(f"Merged data saved to {output_file_path}")
