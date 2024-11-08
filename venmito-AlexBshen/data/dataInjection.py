
import psycopg2
import pandas as pd
from dataRead import load_json,load_csv,load_xml,load_yaml  # Import your data loading function

# Database connection ()
def connect_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Tamarindos100",
        host="localhost",
        port="5432"
    )

    return conn

# #Populate the Clients table with data from people.json
def populate_clients(conn, people_df):
    conn.autocommit = True  # Enable autocommit
    cursor = conn.cursor()
    for _, row in people_df.iterrows():


        # Convert devices list to a comma-separated string
        devices_str = ", ".join(row['devices']) if 'devices' in row and row['devices'] else None

        # Debugging: Print each row's devices string before insertion
        print(f"Inserting Client ID: {row['id']} with devices: {devices_str}")

        cursor.execute("""
        INSERT INTO Clients (client_id, first_name, last_name, telephone, email, city, country, devices)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (client_id) DO NOTHING
        """, (
            row['id'],
            row['first_name'],
            row['last_name'],
            row['telephone'],
            row['email'],
            row['location']['City'],
            row['location']['Country'],
            devices_str 
        ))

        conn.commit()  
    print("Clients table populated successfully.")


# # Populate the Promotions table with data from promotions.csv
def populate_promotions(conn, promotions_df):
    cursor = conn.cursor()




    promotions_df = promotions_df.where(pd.notnull(promotions_df), None)




    # Iterate through each row in the promotions 
    for _, row in promotions_df.iterrows():


        # Retrieve the client_id based on email and telephone
        if row['client_email'] is None or row['telephone'] is None:
            continue

        cursor.execute("""
        SELECT client_id FROM Clients WHERE email = %s AND telephone = %s
        """, (row['client_email'], row['telephone']))
        
        result = cursor.fetchone()
        if result:
            client_id = result[0]
            
            # Insert promotion with the matched client_id
            cursor.execute("""
            INSERT INTO Promotions (client_id, promotion, responded)
            VALUES (%s, %s, %s)
            """, (client_id, row['promotion'], row['responded'] == 'Yes'))
    
    # Commit the changes
    conn.commit()
    print("Promotions table populated successfully.")








# ## function to populate transactions

def populate_transactions(conn, transactions_df):
    cursor = conn.cursor()

    # Iterate over each transaction
    for _, row in transactions_df.iterrows():
        transaction_id = row['id']
        store = row['store']
        phone = row['phone']
        item_name = row['item']
        price = row['price']
        price_per_item = row['price_per_item']
        quantity = row['quantity']
        
        # Retrieve the client_id based on phone number
        cursor.execute("""
        SELECT client_id FROM Clients WHERE telephone = %s
        """, (phone,))
        
        client_result = cursor.fetchone()
        
        if client_result:
            client_id = client_result[0]

            # Check for duplicates in Transactions table
            cursor.execute("""
            SELECT 1 FROM Transactions WHERE transaction_id = %s AND item_name = %s
            """, (transaction_id, item_name))
            exists = cursor.fetchone()

            if not exists:
            # Insert each item in the transaction
                cursor.execute("""
                INSERT INTO Transactions (transaction_id, client_id, store, item_name, price, price_per_item, quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    transaction_id,
                    client_id,
                    store,
                    item_name,
                    float(price),
                    float(price_per_item),
                    int(quantity)
                ))
    
    # Commit the changes
    conn.commit()
    print("Transactions table populated successfully.")






## function to populate transfers
def populate_transfers(conn, transfers_df):
    cursor = conn.cursor()

    # Iterate through each row in the transfers DataFrame
    for _, row in transfers_df.iterrows():
        sender_id = str(row['sender_id']).zfill(4)  # Normalize ID to string with leading zeros
        recipient_id = str(row['recipient_id']).zfill(4)
        amount = float(row['amount'])
        date = row['date']
        
        # Check if both sender and recipient exist in the Clients table
        cursor.execute("SELECT client_id FROM Clients WHERE client_id = %s", (sender_id,))
        sender_result = cursor.fetchone()
        
        cursor.execute("SELECT client_id FROM Clients WHERE client_id = %s", (recipient_id,))
        recipient_result = cursor.fetchone()

        # Only insert if both sender and recipient exist
        if sender_result and recipient_result:
            cursor.execute("""
            INSERT INTO Transfers (sender_id, recipient_id, amount, date)
            VALUES (%s, %s, %s, %s)
            """, (sender_id, recipient_id, float(row['amount']), row['date']))

            print(f"Inserted transfer: {sender_id} -> {recipient_id}, Amount: {amount}, Date: {date}")
        else:
            print(f"Transfer skipped. Sender or recipient not found for IDs: {sender_id}, {recipient_id}")


    # Commit the changes
    conn.commit()
    print("Transfers table populated successfully.")










# Main function to load data and populate tables
if __name__ == "__main__":
    

    conn = connect_database()
    
    # Load data  
    people_df = load_json('C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/people.json')
    promotions_df =load_csv('C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/promotions.csv')
    transactions_df = load_xml('C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/transactions.xml')
    transfers_df = load_csv('C:/Users/lolaa/Downloads/Xtillion/venmito-AlexBshen/data/transfers.csv')

    
    ############## Populate tables ###################################

    #populate clients table
    populate_clients(conn, people_df)

    #populate promotions table
    populate_promotions(conn, promotions_df)



    #populate transactions table
    populate_transactions(conn, transactions_df)

    # populate transfers table
    populate_transfers(conn, transfers_df)

    
    # Close the connection
    conn.close()



