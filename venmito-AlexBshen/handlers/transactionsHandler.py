# handlers/transactions_handler.py
from flask import jsonify,request
import daos.transactionsDAO as transactions_dao

# Get all transactions
def get_all_transactions():
    transactions = transactions_dao.get_all_transactions()
    return jsonify(transactions)



# Get transactions by client_id
def get_transactions_by_client(client_id):
    client_transactions = transactions_dao.get_transactions_by_client(client_id)
    return jsonify(client_transactions)

# Add a new transaction
def add_transaction():
    data = request.get_json()
    response = transactions_dao.add_transaction(
        transaction_id=data['transaction_id'],
        client_id=data['client_id'],
        store=data['store'],
        items=data['items']
    )
    return jsonify(response), 201






############################sStatistics#####################

# Get total revenue per store
def get_total_revenue_per_store():
    revenue_per_store = transactions_dao.get_total_revenue_per_store()
    return jsonify(revenue_per_store)



#  Total Revenue by Item
def get_total_revenue_by_item():
    revenue_by_item = transactions_dao.get_total_revenue_by_item()
    return jsonify(revenue_by_item)





#  Most Sold Items
def get_most_sold_items():
    most_sold_items = transactions_dao.get_most_sold_items()
    return jsonify(most_sold_items)




#  Top Clients by Spending
def get_top_clients_by_spending():
    top_clients = transactions_dao.get_top_clients_by_spending()
    return jsonify(top_clients)



#  Average Transaction Value
def get_average_transaction_value():
    avg_transaction_value = transactions_dao.get_average_transaction_value()
    return jsonify(avg_transaction_value)






# Get Monthly Sales Trends
def get_monthly_sales_trends():
    monthly_trends = transactions_dao.get_monthly_sales_trends()
    return jsonify(monthly_trends)


def get_total_spending_by_region():
    data = transactions_dao.get_total_spending_by_region()
    return jsonify(data)