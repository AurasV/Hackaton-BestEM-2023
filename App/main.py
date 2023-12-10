import os
import json
from flask import Flask, render_template, jsonify
app = Flask(__name__)

# Functions to load JSON data from files in the 'JSONs' folder

categories = [
    "Home Decor & Ornaments",
    "Kitchenware",
    "Stationery",
    "Accessories",
    "Toys & Games",
    "Clothing",
    "Beauty & Care",
    "Art & Collectibles",
    "Garden & Outdoor",
    "Festive & Seasonal",
    "Jewelry & Accessories",
    "Storage & Organization",
    "Baking & Cookware",
    "Crafts & Hobbies",
    "Party & Celebration",
    "Outdoor & Gardening",
    "Fashion & Apparel",
    "Kids & Baby",
    "Hobbies & Leisure",
    "Travel & Luggage",
    "Color Themes",
    "Bathroom & Wellness",
    "Pet Supplies",
    "Electronics",
]


def load_json_data(file_name):
    file_path = os.path.join('JSONs', file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_categories_data(file_name):
    file_path = os.path.join('JSONs\\Categories', file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_all_category_data(folder_path):
    all_category_data = {}

    # List all files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                category_data = json.load(file)
                # Use the file name (without extension) as a key in the dictionary
                all_category_data[file_name.replace('.json', '')] = category_data

    return all_category_data


def load_customer_purchases_data(file_name):
    file_path = os.path.join('JSONs\\Customers Purchases', file_name)
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def load_all_customer_purchases_data(folder_path):
    all_customer_purchases_data = {}

    # List all files in the folder
    files = os.listdir(folder_path)

    for file_name in files:
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                customer_purchases_data = json.load(file)
                # Use the file name (without extension) as a key in the dictionary
                all_customer_purchases_data[file_name.replace('.json', '')] = customer_purchases_data

    return all_customer_purchases_data


def get_customer_ids(folder_path):
    files = os.listdir(folder_path)
    customer_ids = [file_name.replace('.json', '') for file_name in files if file_name.endswith('.json')]
    return customer_ids


@app.route('/')
def home():
    return render_template('login.html')

# Landing page
@app.route('/index')
def index():
    data_sales = load_json_data('monthly_sales_with_desc.json')
    data_revenue = load_json_data('monthly_revenue_with_desc.json')
    return render_template('index.html', data_sales=data_sales, data_revenue=data_revenue)


# Customer dashboard
@app.route('/customer')
def customer_dashboard():
    folder_path = 'JSONs\\Customers Purchases'
    customer_ids = get_customer_ids(folder_path)
    return render_template('customerDashboard.html', customer_ids=customer_ids)


@app.route('/get_customer_data/<customer_id>')
def get_customer_data(customer_id):
    folder_path = 'JSONs\\Customers Purchases'
    file_path = os.path.join(folder_path, f'{customer_id}.json')

    with open(file_path, 'r') as file:
        customer_data = json.load(file)

    return jsonify(customer_data)


# Employee dashboard
@app.route('/employee')
def employee_dashboard():
    data = load_all_category_data('JSONs\\Categories')
    data_sales = load_json_data('monthly_sales_with_desc.json')
    data_revenue = load_json_data('monthly_revenue_with_desc.json')
    return render_template('employeeDashboard.html', categories=categories, data=data, data_sales=data_sales, data_revenue=data_revenue)



if __name__ == '__main__':
    app.run(debug=True)
