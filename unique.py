import json

def remove_duplicates_from_json(input_file_path, output_file_path):
    try:
        # Load the JSON data from the input file
        with open(input_file_path, 'r') as file:
            data = json.load(file)

        # Check if the data is a list
        if not isinstance(data, list):
            raise ValueError("JSON data is not a list")

        # Use a set to track unique descriptions
        unique_descriptions = set()
        unique_data = []

        for entry in data:
            # Check for 'Description' key in each entry
            if 'Description' in entry:
                # Check if the description is unique
                if entry['Description'] not in unique_descriptions:
                    unique_descriptions.add(entry['Description'])
                    unique_data.append(entry)

        # Save the unique data to the output file
        with open(output_file_path, 'w') as file:
            json.dump(unique_data, file, indent=4)

        print("Duplicates removed successfully. Output saved to:", output_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
remove_duplicates_from_json('transactions.json', 'unique.json')
