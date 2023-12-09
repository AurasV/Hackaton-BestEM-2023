import json
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def filter_text(text, additional_exclusions, include_keywords):
    tokens = word_tokenize(text)
    return [word for word in tokens if word in include_keywords or word not in additional_exclusions]

# Define categories and consolidate all keywords
categories = {
    "Home Decor & Ornaments": ["drawers", "drawer", "fan", "magnetic", "bunny", "candle/glass", "candle", "decoration", "jewelled", "stool", "stools", "owl", "polka", "decorative", "dolphins", "cute", "candlestick", "design", "designs", "sand", "animal", "erasers", "magnet", "magnets", "dionsaur", "frog", "t-light", "t-lights", "felt", "willow", "lights.", "led", "torch", "chocolatecandle", "tube", "crystal", "luggage", "knitted", "stool", "ceramic", "curtain", "pad", "jar", "skull", "bird", "wooden", "ivory", "windmill", "feather", "shell", "house", "drawer", "mobile", "pearl", "brown", "fairy", "treasure","door mat", "wood", "hanger", "doorsign", "knob", "lamp", "crochet", "hottie", "heart", "heart.", "light", "figures", "doorstop", "inflatable", "floral", "monster", "bath", "clock", "love", "word", "block", "building", "letters", "home", "block", "assorted", "doormat", "doormats", "decoration", "ornament", "lights", "candle", "holder", "heart", "decoration", "frame", "mirror", "lantern", "vase", "rose", "hanging", "hook", "tile", "incense", "wall", "acrylic", "slate", "photo", "ribbon", "egg", "cabinet", "garland", "lampshade"],
    "Kitchenware": ["coaster", "ladder", "bottle", "bottles", "french", "picture", "holders", "candleholder", "platter", "friends", "fruitbowl", "teapot", "straw", "straws", "chopstick", "chopsticks", "coasters", "mat", "retro", "retrospot", "jug", "milk", "kitchen", "spotty", "storage", "rack", "cup", "pan", "matches", "bowl", "mug", "tray", "dish", "cutlery", "glass", "plate", "apron", "tea"],
    "Stationery": ["envelope", "letter", "rubber", "rubbers", "sticker", "stickers", "notepad", "journal", "journals", "phone", "pencils", "tape", "tag", "pencil", "notebook", "phone", "pencils", "tape", "tag", "pencil", "notebook", "notebook", "pen", "paper", "wrap", "book", "mini", "stickers", "reel"],
    "Accessories": ["backpack", "button", "key", "string", "hand", "scented", "ribbon", "ribbons", "ring", "bracelet", "glove", "gloves", "towel", "towels", "umbrella", "bag", "purse", "wallet", "scarf", "keyring", "earrings", "butterfly", "diamante", "handbag"],
    "Toys & Games": ["car", "jumbo", "alphabet", "jigsaw", "puzzle", "toy", "game", "doll", "set", "pack", "card", "play"],
    "Clothing": ["sombrero", "overall", "ear", "muff", "muffs", "jumper", "shirt", "dress", "top", "skirt", "sweater", "jacket", "hat", "sock", "scarf", "tie"],
    "Beauty & Care": ["soap", "cream", "lotion", "brush", "cosmetic", "makeup", "shampoo", "oil", "spray"],
    "Art & Collectibles": ["design", "sign", "paint", "drawing", "craft", "colour", "design", "art", "print", "painting", "art", "collectible", "vintage", "print", "painting"],
    "Garden & Outdoor": ["pots", "garden", "flower", "plant", "pot", "tool", "basket", "flowers"],
    "Festive & Seasonal": ["toast", "mum", "dad", "christmas", "easter", "halloween", "valentine", "holiday", "seasonal", "celebration", "party", "anniversary", "birthday", "wreath", "christmas", "candles", "easter", "halloween", "valentine", "mother", "father", "day", "birthday", "anniversary", "wedding", "graduation", "party", "new", "year", "easter", "thanksgiving", "holiday", "seasonal"],
    "Jewelry & Accessories": ["necklace", "ring", "bracelet", "earrings", "butterfly", "diamante", "handbag"],
    "Storage & Organization": ["tin", "tins", "bin", "box", "cover", "cushion"],
    "Baking & Cookware": ["chocolate", "egg", "eggs", "biscuits", "cake", "metal"],
    "Crafts & Hobbies": ["feltcraft", "kit", "sketchbook", "plasters", "sweetheart", "enamel", "painting", "drawing", "craft"],
    "Party & Celebration": ["greeting", "party", "celebration", "festival", "anniversary", "birthday"],
    "Outdoor & Gardening": ["shed", "green", "garden", "plant", "flower", "pot", "parasol", "hammock", "picnic", "outdoor", "parasol", "garden", "plant", "flower", "picnic", "outdoor", "hammock", "pot"],
    "Fashion & Apparel": ["charm", "silver", "gold", "hair", "glove", "scarf", "hat", "tie", "rabbit", "girl"],
    "Kids & Baby": ["kids", "baby", "children", "nursery", "toy", "game"],
    "Hobbies & Leisure": ["hobby", "leisure", "activity", "recreation"],
    "Travel & Luggage": ["luggage", "tag", "travel", "bag"],
    "Color Themes": ['pink', 'red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple', 'brown', 'grey', 'gray', 'silver', 'gold'],
    "Bathroom & Wellness": ["bottle", "water", "hot", "bath", "soap", "lotion", "shampoo", "toilet", "bathroom", "towel", "soap", "shampoo", "lotion"],
    "Pet Supplies": ["toy", "ball", "chew", "play", "squeaky", "bowl", "feeder", "water", "dish", "brush", "shampoo", "clipper", "comb", "groom", "bed", "cushion", "blanket", "pillow", "collar", "leash", "harness", "lead", "tag", "supplement", "medication", "treatment", "care", "health", "coat", "clothing", "boot", "cap", "vest", "clicker", "training"],
    "Electronics": ["phone", "tablet", "laptop", "computer", "camera", "printer", "scanner", "tv", "television", "monitor", "smartwatch", "mobile"],
}

all_keywords = set()
for keywords in categories.values():
    all_keywords.update([keyword.lower() for keyword in keywords])  # Convert keywords to lowercase

# Load the JSON data
file_path = 'transactions.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Define additional words to exclude (not including the keywords)
additional_exclusions = {
    'pink', 'red', 'blue', 'green', 'black', 'white', 'yellow', 'orange', 'purple', 'brown',
    'grey', 'gray', 'silver', 'gold', '', 'w', "'s", "'re", "'ve", "'ll", "'d", "n't", "''", "``", "'m", "“", "”", ",", "&"
}

# Process each item in the data
word_count = {}
for item in data:
    if 'Description' in item:
        filtered_description = filter_text(item['Description'].lower(), additional_exclusions, all_keywords)
        for word in filtered_description:
            if not re.match(r'^\d+$', word) and word not in stopwords.words('english'):
                word_count[word] = word_count.get(word, 0) + 1

# Map words to categories
word_to_category = {}
for category, keywords in categories.items():
    for keyword in keywords:
        if keyword.lower() in word_count:
            word_to_category[keyword.lower()] = category

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
output_file_path = 'transactions_with_categories.json'
with open(output_file_path, 'w') as file:
    json.dump(data, file, indent=4)
