from config import get_db_connection


# Get all transactions with item details
def get_all_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, t.store, t.item_name, t.price, t.price_per_item, t.quantity, c.telephone
        FROM Transactions t
        JOIN Clients c ON t.client_id = c.client_id
        ORDER BY t.transaction_id;
    """)
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return transactions






# Get transactions by client_id
def get_transactions_by_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaction_id, store, item_name, price, price_per_item, quantity
        FROM Transactions
        WHERE client_id = %s;
    """, (client_id,))
    client_transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return client_transactions





# Add a new transaction
def add_transaction(transaction_id, client_id, store, items):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert each item in the transaction
    for item in items:
        cursor.execute("""
            INSERT INTO Transactions (transaction_id, client_id, store, item_name, price, price_per_item, quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            transaction_id,
            client_id,
            store,
            item['item_name'],
            item['price'],
            item['price_per_item'],
            item['quantity']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Transaction added successfully", "transaction_id": transaction_id}



#############################Statistics

# Get total revenue per store
def get_total_revenue_per_store():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT store, SUM(price * quantity) AS total_revenue
        FROM Transactions
        GROUP BY store
        ORDER BY total_revenue DESC;
    """)
    revenue_per_store = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"store": row[0], "total_revenue": row[1]} for row in revenue_per_store]





#  Total Revenue by Item
def get_total_revenue_by_item():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT item_name, SUM(price * quantity) AS total_revenue
        FROM Transactions
        GROUP BY item_name
        ORDER BY total_revenue DESC;
    """)
    revenue_by_item = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"item_name": row[0], "total_revenue": row[1]} for row in revenue_by_item]




#  Most Sold Items
def get_most_sold_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT item_name, SUM(quantity) AS total_quantity
        FROM Transactions
        GROUP BY item_name
        ORDER BY total_quantity DESC;
    """)
    most_sold_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"item_name": row[0], "total_quantity": row[1]} for row in most_sold_items]




#  Top Clients by Spending
def get_top_clients_by_spending():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.client_id, c.first_name, c.last_name, SUM(t.price * t.quantity) AS total_spending
        FROM Transactions t
        JOIN Clients c ON t.client_id = c.client_id
        GROUP BY c.client_id, c.first_name, c.last_name
        ORDER BY total_spending DESC;
    """)
    top_clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"client_id": row[0], "first_name": row[1], "last_name": row[2], "total_spending": row[3]} for row in top_clients]




#  Average Transaction Value
def get_average_transaction_value():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ROUND(AVG(price * quantity)::numeric, 2) AS avg_transaction_value
        FROM Transactions;
    """)
    avg_transaction_value = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"average_transaction_value": avg_transaction_value}


# 3. Identify High-Value Clients (top spenders)
def get_top_spenders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.client_id, c.first_name, c.last_name, SUM(t.price * t.quantity) AS total_spent
        FROM Clients c
        JOIN Transactions t ON c.client_id = t.client_id
        GROUP BY c.client_id
        ORDER BY total_spent DESC
        LIMIT 10;
    """)
    top_spenders = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"client_id": row[0], "first_name": row[1], "last_name": row[2], "total_spent": row[3]} for row in top_spenders]




# Total Spending by Country and City
def get_total_spending_by_region():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT country, city, SUM(t.price * t.quantity) AS total_spent
        FROM Transactions t
        JOIN Clients c ON t.client_id = c.client_id
        GROUP BY country, city
        ORDER BY total_spent DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"country": row[0], "city": row[1], "total_spent": row[2]} for row in results]
