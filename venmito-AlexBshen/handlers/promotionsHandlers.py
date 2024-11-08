from flask import jsonify, request
import daos.promotionsDAO as promotions_dao

# Get all promotions
def get_all_promotions():
    promotions = promotions_dao.get_all_promotions()
    return jsonify(promotions)





# Get promotions by client_id
def get_promotions_by_client(client_id):
    client_promotions = promotions_dao.get_promotions_by_client(client_id)
    return jsonify(client_promotions)





# Add a new promotion
def add_promotion():
    data = request.get_json()
    response = promotions_dao.add_promotion(
        client_id=data['client_id'],
        promotion=data['promotion'],
        responded=data.get('responded', False)  # Defaults to False if not provided
    )
    return jsonify(response), 201






# Update promotion response
def update_promotion_response(promotion_id):
    data = request.get_json()
    responded = data.get('responded')
    if responded is None:
        return jsonify({"error": "Missing 'responded' field"}), 400
    response = promotions_dao.update_promotion_response(promotion_id, responded)
    return jsonify(response)






# Delete a promotion
def delete_promotion(promotion_id):
    response = promotions_dao.delete_promotion(promotion_id)
    return jsonify(response)





#################################################################################
######################## Statistics #############################################
################################################################################


# Get overall promotion engagement rate
def get_overall_engagement_rate():
    engagement_rate = promotions_dao.get_overall_engagement_rate()
    return jsonify(engagement_rate)

# Get engagement rate by promotion type
def get_engagement_rate_by_promotion_type():
    engagement_rates = promotions_dao.get_engagement_rate_by_promotion_type()
    return jsonify(engagement_rates)

# Get clients with no responses
def get_non_responding_clients():
    non_responding_clients = promotions_dao.get_non_responding_clients()
    return jsonify(non_responding_clients)

# Get top promotion types by response count
def get_top_promotion_types():
    top_promotions = promotions_dao.get_top_promotion_types()
    return jsonify(top_promotions)



# Get Conversion Rate by Promotion Type
def get_conversion_rate_by_promotion_type():
    conversion_rates = promotions_dao.get_conversion_rate_by_promotion_type()
    return jsonify(conversion_rates)


## most effective promotions
def get_top_promotions():
    promotions = promotions_dao.get_top_promotions()
    return jsonify(promotions)


def get_promotion_engagement_by_country():
    data = promotions_dao.get_promotion_engagement_by_country()
    return jsonify(data)