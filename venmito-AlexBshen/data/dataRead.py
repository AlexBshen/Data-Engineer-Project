import json ## pip install
import yaml ## pip install
import pandas as pd ## pip install
import xml.etree.ElementTree as ET

# 1. Load JSON file (people.json)
def load_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

# 2. Load YAML file (people.yml)
def load_yaml(filepath):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return pd.DataFrame(data)

# 3. Load CSV file (transfers.csv or promotions.csv)
def load_csv(filepath):
    return pd.read_csv(filepath)





# 4. Load XML file (transactions.xml)
def load_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    transactions = []
    
    # Iterate through each transaction element
    for transaction in root.findall('transaction'):
        transaction_id = transaction.get('id')
        store = transaction.find('store').text
        phone = transaction.find('phone').text

        # Extract items within each transaction
   
        for item in transaction.find('items'):
            item_name = item.find('item').text
            price = item.find('price').text
            price_per_item = item.find('price_per_item').text
            quantity = item.find('quantity').text
            
            # Append each item as a dictionary with transaction details
            transactions.append({
                'id': transaction_id,
                'store': store,
                'phone': phone,
                'item': item_name,
                'price': float(price),
                'price_per_item': float(price_per_item),
                'quantity': int(quantity)
            })
        

    
    # Convert the list of transactions to a DataFrame
    return pd.DataFrame(transactions)












# Paths to files
json_path = 'C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/people.json'
yaml_path = 'C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/people.yml'
csv_transfers_path = 'C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/transfers.csv'
csv_promotions_path = 'C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/promotions.csv'
xml_path = 'C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/transactions.xml'

# Load data
people_json_df = load_json(json_path)
people_yaml_df = load_yaml(yaml_path)
transfers_df = load_csv(csv_transfers_path)
promotions_df = load_csv(csv_promotions_path)
transactions_df = load_xml(xml_path)

# # Display sample data
print("People (JSON):", people_json_df.head()) ##/head() displays first 5 by default
print("People (YAML):", people_yaml_df.head())
print("Transfers (CSV):", transfers_df.head())
print("Promotions (CSV):", promotions_df.head())
print("Transactions (XML):", transactions_df.head())
