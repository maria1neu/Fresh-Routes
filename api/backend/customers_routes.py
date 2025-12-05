from flask import Blueprint, request, jsonify

customers_routes = Blueprint('customers_routes', __name__)

@customers_routes.post("customers")
def create_customer():
    data = request.json
    return jsonify({"message": "Customer created", "data": data})


@customers_routes.get("/customers/<int:customer_id>")
def get_customer(customer_id):
    return jsonify({"message": "Get customer profile", "customer_id": customer_id})


@customers_routes.put("/customers/<int:customer_id>")
def update_customer(customer_id):
    data = request.json
    return jsonify({"message": "Update customer preferences", "customer_id": customer_id, "data": data})

@customers_routes.delete("/customers/<int:customer_id>")
def delete_customer(customer_id):
    return jsonify({"message": "Delete customer account", "customer_id": customer_id})


@customers_routes.get("/customers/<int:customer_id>/notifications")
def get_notifications(customer_id):
    return jsonify({"message": "Get notifications", "customer_id": customer_id})

@customers_routes.get("/customers/<int:customer_id>/messages")
def get_customer_messages(customer_id):
    return jsonify({"message": "Get customer messages", "customer_id": customer_id})


@customers_routes.post("/customers/<int:customer_id>/messages")
def send_customer_message(customer_id):
    data = request.json
    return jsonify({"message": "Send customer message", "customer_id": customer_id, "data": data})