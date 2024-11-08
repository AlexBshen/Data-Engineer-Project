from config import get_db_connection

# Get all clients
def get_all_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return clients






# Get client by ID
def get_client_by_id(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()
    conn.close()
    return client





# Search clients by city or country
def search_clients_by_location(city=None, country=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if city and country:
        cursor.execute("SELECT * FROM Clients WHERE city = %s AND country = %s", (city, country))
    elif city:
        cursor.execute("SELECT * FROM Clients WHERE city = %s", (city,))
    elif country:
        cursor.execute("SELECT * FROM Clients WHERE country = %s", (country,))
    else:
        return []  # No city or country provided

    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return clients




# Add a new client
def add_client(client_id, first_name, last_name, telephone, email, city, country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clients (client_id, first_name, last_name, telephone, email, city, country)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (client_id, first_name, last_name, telephone, email, city, country))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Client added successfully"}







# Update client information
def update_client(client_id, first_name, last_name, telephone, email, city, country):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Clients
        SET first_name = %s, last_name = %s, telephone = %s, email = %s, city = %s, country = %s
        WHERE client_id = %s
    """, (first_name, last_name, telephone, email, city, country, client_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Client updated successfully"}







# Delete a client
def delete_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Clients WHERE client_id = %s", (client_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Client deleted successfully"}






# Count clients by country
def count_clients_by_country():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT country, COUNT(*) AS client_count
        FROM Clients
        GROUP BY country
        ORDER BY client_count DESC;
    """)
    client_counts_by_country = cursor.fetchall()
    cursor.close()
    conn.close()
    return client_counts_by_country



# Count clients by city and country
def count_clients_by_city_and_country():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT country, city, COUNT(*) AS client_count
        FROM Clients
        GROUP BY country, city
        ORDER BY client_count DESC;
    """)
    client_counts_by_city_and_country = cursor.fetchall()
    cursor.close()
    conn.close()
    return client_counts_by_city_and_country


## Top engaged clients by transaction and transfers frequency
def get_top_engaged_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.client_id, c.first_name, c.last_name, COUNT(t.transaction_id) + COUNT(r.transfer_id) AS engagement_score
        FROM Clients c
        LEFT JOIN Transactions t ON c.client_id = t.client_id
        LEFT JOIN Transfers r ON c.client_id = r.sender_id OR c.client_id = r.recipient_id
        GROUP BY c.client_id
        ORDER BY engagement_score DESC
        LIMIT 10;
    """)
    top_clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"client_id": row[0], "first_name": row[1], "last_name": row[2], "engagement_score": row[3]} for row in top_clients]




