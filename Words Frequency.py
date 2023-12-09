import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Function to preprocess and filter out specific POS tags
def filter_pos(text, excluded_tags, additional_exclusions):
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    return [word for word, tag in tagged if tag not in excluded_tags and word not in additional_exclusions]

# Load the JSON data from the uploaded file
file_path = 'unique.json'

with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize a dictionary to count the occurrences of each word
word_count = {}

# Tags to exclude (e.g., adjectives and adverbs)
excluded_tags = {'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'}

# Additional words to exclude (e.g., colors, common terms, and non-informative fragments)
additional_exclusions = {
    'pink', 'red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple', 'brown',
    'grey', 'gray', 'silver', 'gold', '', 'w', "'s", "'re", "'ve", "'ll", "'d", "n't", "''", "``", "'m", "“", "”", ",", "&"
}

for item in data:
    if 'Description' in item:
        # Preprocess and filter words based on POS tags and additional exclusions
        filtered_description = filter_pos(item['Description'].lower(), excluded_tags, additional_exclusions)
        for word in filtered_description:
            if not re.match(r'^\d+$', word) and word not in stopwords.words('english'):
                word_count[word] = word_count.get(word, 0) + 1

# Sort the words by their frequency, in descending order
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

# Filter to keep words with at least 20 mentions
filtered_words = [(word, count) for word, count in sorted_words if count >= 20]

# Write the filtered words to a file
output_file_path = 'filtered_words.txt'

with open(output_file_path, 'w') as file:
    for word, count in filtered_words:
        file.write(f"{word}: {count}\n")
