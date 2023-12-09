import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def filter_pos(text, excluded_tags, additional_exclusions):
    tokens = word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    return [word for word, tag in tagged if tag not in excluded_tags and word not in additional_exclusions]

# Load the JSON data
file_path = 'unique.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize a dictionary to count the occurrences of each word
word_count = {}

# Define tags and additional words to exclude
excluded_tags = {'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'}
additional_exclusions = {
    'pink', 'red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple', 'brown',
    'grey', 'gray', 'silver', 'gold', '', 'w', "'s", "'re", "'ve", "'ll", "'d", "n't", "''", "``", "'m", "“", "”", ",", "&"
}
# Process each item in the data
for item in data:
    if 'Description' in item:
        filtered_description = filter_pos(item['Description'].lower(), excluded_tags, additional_exclusions)
        for word in filtered_description:
            if not re.match(r'^\d+$', word) and word not in stopwords.words('english'):
                word_count[word] = word_count.get(word, 0) + 1

# Sort and filter words
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
filtered_words = [(word, count) for word, count in sorted_words if count >= 20]

# Define categories
categories = {
    "Home Decor & Ornaments": ["inflatable", "floral", "monster", "bath", "clock", "love", "word", "block", "building", "letters", "home", "block", "assorted", "doormat", "doormats", "decoration", "ornament", "lights", "candle", "holder", "heart", "decoration", "frame", "mirror", "lantern", "vase"],
    "Kitchenware": ["bowl", "mug", "tray", "dish", "cutlery", "glass", "plate"],
    "Stationery": ["notebook", "pen", "paper", "card", "wrap", "book"],
    "Accessories": ["bag", "purse", "wallet", "scarf", "keyring"],
    "Toys & Games": ["toy", "game", "doll", "set", "pack", "card", "play"],
    "Clothing": ["shirt", "dress", "top", "skirt", "sweater", "jacket", "hat", "sock", "scarf", "tie"],
    "Beauty & Care": ["soap", "cream", "lotion", "brush", "cosmetic", "makeup", "shampoo", "oil", "spray"],
    "Art & Collectibles": ["art", "collectible", "vintage", "print", "painting"],
    "Garden & Outdoor": ["garden", "flower", "plant", "pot", "tool"],
    "Festive & Seasonal": ["christmas", "candles", "easter", "halloween", "valentine", "mother", "father", "day", "birthday", "anniversary", "wedding", "graduation", "party", "new", "year", "easter", "thanksgiving", "holiday", "seasonal"],
    "Jewelry & Accessories": ["necklace"],
    "Storage & Organization": ["box", "cover", "cushion"],
    "Baking & Cookware": ["cake", "metal"],
    "Color Themes": ["pink", "blue", "red", "white", "black", "green"],
    "Art & Decor": ["design", "sign"],
    "Pet Supplies": ["toy", "ball", "chew", "play", "squeaky", "bowl", "feeder", "water", "dish", "brush", "shampoo", "clipper", "comb", "groom", "bed", "mat", "cushion", "blanket", "pillow", "collar", "leash", "harness", "lead", "tag", "supplement", "medication", "treatment", "care", "health", "coat", "clothing", "boot", "cap", "vest", "clicker", "training"],
    "Sizes & Dimensions": ["small", "large"],
}

# Map words to categories
word_to_category = {}
for category, keywords in categories.items():
    for keyword in keywords:
        if keyword in [word for word, count in filtered_words]:
            word_to_category[keyword] = category

# Function to assign a category
def assign_category(description):
    words = description.lower().split()
    for word in words:
        if word in word_to_category:
            return word_to_category[word]
    return "Other"

# Assign categories to JSON data
for item in data:
    if 'Description' in item:
        item['Category'] = assign_category(item['Description'])

# Write to a new JSON file
output_file_path = 'unique_with_categories.json'
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)
