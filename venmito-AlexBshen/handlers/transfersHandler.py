from flask import jsonify,request

import daos.transfersDAO as transfers_dao



# Get all transfers
def get_all_transfers():
    transfers = transfers_dao.get_all_transfers()
    return jsonify(transfers)

#  Get transfers by sender_id
def get_transfers_by_sender(sender_id):
    sender_transfers = transfers_dao.get_transfers_by_sender(sender_id)
    return jsonify(sender_transfers)

#  Add a new transfer
def add_transfer():
    data = request.get_json()
    response = transfers_dao.add_transfer(
        sender_id=data['sender_id'],
        recipient_id=data['recipient_id'],
        amount=data['amount'],
        date=data['date']
    )
    return jsonify(response), 201





## statitscs

#  Get total transfer amount by sender
def get_total_transfer_amount_by_sender():
    transfer_amounts = transfers_dao.get_total_transfer_amount_by_sender()
    return jsonify(transfer_amounts)





# Top Recipients by Received Amount
def get_top_recipients_by_received_amount():
    top_recipients = transfers_dao.get_top_recipients_by_received_amount()
    return jsonify(top_recipients)




# Average Transfer Amount
def get_average_transfer_amount():
    avg_transfer_amount = transfers_dao.get_average_transfer_amount()
    return jsonify(avg_transfer_amount)





# Monthly Transfer Volume
def get_monthly_transfer_volume():
    monthly_volume = transfers_dao.get_monthly_transfer_volume()
    return jsonify(monthly_volume)




# Most Frequent Senders
def get_most_frequent_senders():
    frequent_senders = transfers_dao.get_most_frequent_senders()
    return jsonify(frequent_senders)