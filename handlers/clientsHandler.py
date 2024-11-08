# handlers/clients_handler.py
from flask import jsonify, request
import daos.clientsDAO as clients_dao

# Get all clients
def get_clients():
    clients = clients_dao.get_all_clients()
    return jsonify(clients)






# Get client by ID
def get_client_by_id(client_id):
    client = clients_dao.get_client_by_id(client_id)
    if client:
        return jsonify(client)
    else:
        return jsonify({"error": "Client not found"}), 404







# Search clients by city or country
def search_clients_by_location():
    city = request.args.get('city')
    country = request.args.get('country')
    clients = clients_dao.search_clients_by_location(city, country)
    return jsonify(clients)







# Add a new client
def add_client():
    data = request.get_json()
    response = clients_dao.add_client(
        client_id=data['client_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        telephone=data['telephone'],
        email=data['email'],
        city=data['city'],
        country=data['country']
    )
    return jsonify(response), 201








# Update client information
def update_client(client_id):
    data = request.get_json()
    response = clients_dao.update_client(
        client_id=client_id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        telephone=data['telephone'],
        email=data['email'],
        city=data['city'],
        country=data['country']
    )
    return jsonify(response)









# Delete a client
def delete_client(client_id):
    response = clients_dao.delete_client(client_id)
    return jsonify(response)







# Get client count by country
def get_client_count_by_country():
    client_counts = clients_dao.count_clients_by_country()
    return jsonify(client_counts)

# Get client count by city and country
def get_client_count_by_city_and_country():
    client_counts = clients_dao.count_clients_by_city_and_country()
    return jsonify(client_counts)



# Get Top Engaged Clients
def get_top_engaged_clients():
    top_clients = clients_dao.get_top_engaged_clients()
    return jsonify(top_clients)


