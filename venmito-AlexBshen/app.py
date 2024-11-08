from flask import Flask, request
from handlers import clientsHandler, transactionsHandler, transfersHandler, promotionsHandlers
# from config import get_db_connection





app = Flask(__name__)

##################################################### Client Endpoints
# Clients Endpoints
@app.route('/clients', methods=['GET'])
def get_clients():
    return clientsHandler.get_clients()




## get client by id
@app.route('/clients/<client_id>', methods=['GET'])
def get_client_by_id(client_id):
    return clientsHandler.get_client_by_id(client_id)





##search by location or country
@app.route('/clients/search', methods=['GET'])
def search_clients_by_location():
    return clientsHandler.search_clients_by_location()



##create new client
@app.route('/clients', methods=['POST'])
def add_client():
    return clientsHandler.add_client()



##update a client by id
@app.route('/clients/<client_id>', methods=['PUT'])
def update_client(client_id):
    return clientsHandler.update_client(client_id)




##delete a client (NOT DESIRABLE)
@app.route('/clients/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    return clientsHandler.delete_client(client_id)






# Client demographics endpoints
@app.route('/clients/demographics/country', methods=['GET'])
def get_client_count_by_country():
    return clientsHandler.get_client_count_by_country()

@app.route('/clients/demographics/city_country', methods=['GET'])
def get_client_count_by_city_and_country():
    return clientsHandler.get_client_count_by_city_and_country()






@app.route('/clients/stats/top_engaged_clients', methods=['GET'])
def get_top_engaged_clients():
    return clientsHandler.get_top_engaged_clients()







############################################################### Transaction Endpoints
@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    return transactionsHandler.get_all_transactions()

@app.route('/transactions/<client_id>', methods=['GET']) ## empty array
def get_transactions_by_client(client_id):
    return transactionsHandler.get_transactions_by_client(client_id)

@app.route('/transactions', methods=['POST'])
def add_transaction():
    return transactionsHandler.add_transaction()




####### statistics
@app.route('/transactions/stats/revenue_per_store', methods=['GET'])
def get_total_revenue_per_store():
    return transactionsHandler.get_total_revenue_per_store()


@app.route('/transactions/stats/revenue_by_item', methods=['GET'])
def get_total_revenue_by_item():
    return transactionsHandler.get_total_revenue_by_item()

@app.route('/transactions/stats/most_sold_items', methods=['GET'])
def get_most_sold_items():
    return transactionsHandler.get_most_sold_items()

@app.route('/transactions/stats/top_clients', methods=['GET'])
def get_top_clients_by_spending():
    return transactionsHandler.get_top_clients_by_spending()

@app.route('/transactions/stats/average_transaction_value', methods=['GET'])
def get_average_transaction_value():
    return transactionsHandler.get_average_transaction_value()




# 4. Monthly Sales Trends
@app.route('/transactions/stats/monthly_sales_trends', methods=['GET'])
def get_monthly_sales_trends():
    return transactionsHandler.get_monthly_sales_trends()







########################################################### Promotions Endpoints

@app.route('/promotions', methods=['GET'])
def get_all_promotions():
    return promotionsHandlers.get_all_promotions()



@app.route('/promotions/<client_id>', methods=['GET']) ## not working
def get_promotions_by_client(client_id):
    return promotionsHandlers.get_promotions_by_client(client_id)



@app.route('/promotions', methods=['POST'])
def add_promotion():
    return promotionsHandlers.add_promotion()



@app.route('/promotions/<promotion_id>', methods=['PUT'])
def update_promotion_response(promotion_id):
    return promotionsHandlers.update_promotion_response(promotion_id)



@app.route('/promotions/<promotion_id>', methods=['DELETE'])
def delete_promotion(promotion_id):
    return promotionsHandlers.delete_promotion(promotion_id)




# Promotions statistics endpoints
@app.route('/promotions/stats/overall_engagement', methods=['GET'])
def get_overall_engagement_rate():
    return promotionsHandlers.get_overall_engagement_rate()


@app.route('/promotions/stats/engagement_by_type', methods=['GET'])
def get_engagement_rate_by_promotion_type():
    return promotionsHandlers.get_engagement_rate_by_promotion_type()


@app.route('/promotions/stats/non_responding_clients', methods=['GET'])
def get_non_responding_clients():
    return promotionsHandlers.get_non_responding_clients()


@app.route('/promotions/stats/top_promotion_types', methods=['GET'])
def get_top_promotion_types():
    return promotionsHandlers.get_top_promotion_types()



@app.route('/promotions/stats/conversion_rate_by_type', methods=['GET'])
def get_conversion_rate_by_promotion_type():
    return promotionsHandlers.get_conversion_rate_by_promotion_type()



## most effective promotions
@app.route('/top_promotions', methods=['GET'])
def get_top_promotions():
    return promotionsHandlers.get_top_promotions()



# ############################################################Transfers Endpoints
#  Get all transfers
@app.route('/transfers', methods=['GET'])
def get_all_transfers():
    return transfersHandler.get_all_transfers()

#  Get transfers by sender_id
@app.route('/transfers/<sender_id>', methods=['GET'])
def get_transfers_by_sender(sender_id):
    return transfersHandler.get_transfers_by_sender(sender_id)



# create new transfer
@app.route('/transfers', methods=['POST'])
def add_transfer():
    return transfersHandler.add_transfer()


## total amount by sender 
@app.route('/transfers/stats/total_amount_by_sender', methods=['GET'])
def get_total_transfer_amount_by_sender():
    return transfersHandler.get_total_transfer_amount_by_sender()



## top recipient by received amount
@app.route('/transfers/stats/top_recipients', methods=['GET'])
def get_top_recipients_by_received_amount():
    return transfersHandler.get_top_recipients_by_received_amount()



## AVerage amount in a transfer
@app.route('/transfers/stats/average_transfer_amount', methods=['GET'])
def get_average_transfer_amount():
    return transfersHandler.get_average_transfer_amount()


##monthly volume transfers
@app.route('/transfers/stats/monthly_volume', methods=['GET'])
def get_monthly_transfer_volume():
    return transfersHandler.get_monthly_transfer_volume()



## most frequent senders
@app.route('/transfers/stats/most_frequent_senders', methods=['GET'])
def get_most_frequent_senders():
    return transfersHandler.get_most_frequent_senders()











########################### Some insights


# Total Spending by Country and City
@app.route('/clients/total_spending_by_region', methods=['GET'])
def get_total_spending_by_region():
    return transactionsHandler.get_total_spending_by_region()

#  Promotion Engagement by Country
@app.route('/promotions/engagement_by_country', methods=['GET'])
def get_promotion_engagement_by_country():
    return promotionsHandlers.get_promotion_engagement_by_country()





if __name__ == '__main__':
    app.run(debug=True,port = 5001)
