from config import get_db_connection

# Get all promotions
def get_all_promotions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.promotion_id, c.client_id, c.email, c.telephone, p.promotion, p.responded
        FROM Promotions p
        JOIN Clients c ON p.client_id = c.client_id;
    """)
    promotions = cursor.fetchall()
    cursor.close()
    conn.close()
    return promotions






# Get promotions by client_id
def get_promotions_by_client(client_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT promotion_id, promotion, responded
        FROM Promotions
        WHERE client_id = %s;
    """, (client_id,))
    client_promotions = cursor.fetchall()
    cursor.close()
    conn.close()
    return client_promotions






# Add a new promotion
def add_promotion(client_id, promotion, responded):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Promotions (client_id, promotion, responded)
        VALUES (%s, %s, %s)
        RETURNING promotion_id;
    """, (client_id, promotion, responded))
    promotion_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Promotion added successfully", "promotion_id": promotion_id}







# Update promotion response
def update_promotion_response(promotion_id, responded):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Promotions
        SET responded = %s
        WHERE promotion_id = %s;
    """, (responded, promotion_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Promotion response updated successfully"}








# Delete a promotion
def delete_promotion(promotion_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Promotions WHERE promotion_id = %s;", (promotion_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Promotion deleted successfully"}






#################################################################################
######################## Statistics #############################################
################################################################################

# daos/promotions_dao.py

# Calculate overall promotion engagement rate
def get_overall_engagement_rate():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            ROUND(100.0 * SUM(CASE WHEN responded = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS engagement_rate
        FROM Promotions;
    """)
    engagement_rate = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {"overall_engagement_rate": engagement_rate}




# Calculate engagement rate by promotion type
def get_engagement_rate_by_promotion_type():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            promotion,
            ROUND(100.0 * SUM(CASE WHEN responded = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS engagement_rate
        FROM Promotions
        GROUP BY promotion
        ORDER BY engagement_rate DESC;
    """)
    engagement_rates = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"promotion": row[0], "engagement_rate": row[1]} for row in engagement_rates]






# Clients with no responses
def get_non_responding_clients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT c.client_id, c.first_name, c.last_name
        FROM Clients c
        LEFT JOIN Promotions p ON c.client_id = p.client_id
        WHERE p.responded = FALSE OR p.responded IS NULL;
    """)
    non_responding_clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return non_responding_clients






# Top promotion types by response count
def get_top_promotion_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT promotion, COUNT(*) AS response_count
        FROM Promotions
        WHERE responded = TRUE
        GROUP BY promotion
        ORDER BY response_count DESC;
    """)
    top_promotions = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"promotion": row[0], "response_count": row[1]} for row in top_promotions]


## conversion rate by promotion type
def get_conversion_rate_by_promotion_type():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT promotion, 
               SUM(CASE WHEN responded THEN 1 ELSE 0 END)::float / COUNT(*) AS conversion_rate
        FROM Promotions
        GROUP BY promotion
        ORDER BY conversion_rate DESC;
    """)
    conversion_rates = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"promotion": row[0], "conversion_rate": round(row[1], 2)} for row in conversion_rates]



## most effective promotions
def get_top_promotions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT promotion, COUNT(*) AS engagement_count
        FROM Promotions
        WHERE responded = TRUE
        GROUP BY promotion
        ORDER BY engagement_count DESC
        LIMIT 5;
    """)
    promotions = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"promotion": row[0], "engagement_count": row[1]} for row in promotions]



#  Promotion Engagement by Country
def get_promotion_engagement_by_country():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.country, COUNT(p.promotion_id) AS total_promotions, 
               SUM(CASE WHEN p.responded THEN 1 ELSE 0 END) AS responded_promotions
        FROM Promotions p
        JOIN Clients c ON p.client_id = c.client_id
        GROUP BY c.country
        ORDER BY total_promotions DESC;
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"country": row[0], "total_promotions": row[1], "responded_promotions": row[2]} for row in results]
