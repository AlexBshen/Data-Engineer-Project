from config import get_db_connection

#  Get all transfers
def get_all_transfers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transfer_id, sender_id, recipient_id, amount, date
        FROM Transfers
        ORDER BY date DESC;
    """)
    transfers = cursor.fetchall()
    cursor.close()
    conn.close()
    return transfers





#  Get transfers by sender_id
def get_transfers_by_sender(sender_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transfer_id, recipient_id, amount, date
        FROM Transfers
        WHERE sender_id = %s
        ORDER BY date DESC;
    """, (sender_id,))
    sender_transfers = cursor.fetchall()
    cursor.close()
    conn.close()
    return sender_transfers





# Add a new transfer
def add_transfer(sender_id, recipient_id, amount, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Transfers (sender_id, recipient_id, amount, date)
        VALUES (%s, %s, %s, %s)
        RETURNING transfer_id;
    """, (sender_id, recipient_id, amount, date))
    transfer_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Transfer added successfully", "transfer_id": transfer_id}






## statistics

# Calculate total transfer amounts by sender
def get_total_transfer_amount_by_sender():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender_id, SUM(amount) AS total_amount
        FROM Transfers
        GROUP BY sender_id
        ORDER BY total_amount DESC;
    """)
    transfer_amounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"sender_id": row[0], "total_amount": row[1]} for row in transfer_amounts]



# Top Recipients by Received Amount
def get_top_recipients_by_received_amount():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT recipient_id, SUM(amount) AS total_received
        FROM Transfers
        GROUP BY recipient_id
        ORDER BY total_received DESC;
    """)
    recipients = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"recipient_id": row[0], "total_received": row[1]} for row in recipients]






#  Average Transfer Amount
def get_average_transfer_amount():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ROUND(AVG(amount)::numeric, 2) AS avg_transfer_amount
        FROM Transfers;
    """)
    avg_transfer_amount = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"average_transfer_amount": avg_transfer_amount}






# Total Transfer Volume Over Time (Monthly)
def get_monthly_transfer_volume():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DATE_TRUNC('month', date::date) AS month, SUM(amount) AS monthly_volume
        FROM Transfers
        GROUP BY month
        ORDER BY month;
    """)
    monthly_volume = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"month": row[0], "monthly_volume": row[1]} for row in monthly_volume]





#  Most Frequent Senders
def get_most_frequent_senders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender_id, COUNT(*) AS transfer_count
        FROM Transfers
        GROUP BY sender_id
        ORDER BY transfer_count DESC;
    """)
    frequent_senders = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"sender_id": row[0], "transfer_count": row[1]} for row in frequent_senders]



