from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error
from flask import current_app

# Blueprint for customer-facing routes
customer_routes = Blueprint("customer_routes", __name__)

@customer_routes.route("/customers", methods=["POST"])
def create_customer():
    try:
        data = request.get_json()

        required_fields = ["customerID", "firstName", "lastName",
                           "dietaryPref", "nutritionGoals", "email"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO Customer (customerID, firstName, lastName,
                                  dietaryPref, nutritionGoals, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data["customerID"],
                data["firstName"],
                data["lastName"],
                data["dietaryPref"],
                data["nutritionGoals"],
                data["email"],
            ),
        )

        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute(
            """
            SELECT customerID, firstName, lastName,
                   dietaryPref, nutritionGoals, email
            FROM Customer
            WHERE customerID = %s
            """,
            (customer_id,),
        )
        customer = cursor.fetchone()
        cursor.close()

        if not customer:
            return jsonify({"error": "Customer not found"}), 404

        return jsonify(customer), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    try:
        data = request.get_json()

        # Only allow updating a clear set of fields
        allowed_fields = ["dietaryPref", "nutritionGoals", "email"]
        update_fields = []
        params = []

        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        # Make sure the customer exists
        cursor.execute(
            "SELECT customerID FROM Customer WHERE customerID = %s",
            (customer_id,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Customer not found"}), 404

        params.append(customer_id)
        query = f"UPDATE Customer SET {', '.join(update_fields)} WHERE customerID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        cursor = db.get_db().cursor()

        cursor.execute(
            "SELECT customerID FROM Customer WHERE customerID = %s",
            (customer_id,),
        )
        if not cursor.fetchone():
            cursor.close()
            return jsonify({"error": "Customer not found"}), 404

        cursor.execute("DELETE FROM Customer WHERE customerID = %s", (customer_id,))
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Customer deleted successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>/notifications", methods=["GET"])
def get_customer_notifications(customer_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        query = """
            SELECT notificationID, timestamp, message, FarmerID, customerID
            FROM Notification
            WHERE customerID = %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (customer_id,))
        notifications = cursor.fetchall()
        cursor.close()

        return jsonify(notifications), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>/messages", methods=["GET"])
def get_customer_messages(customer_id):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        query = """
            SELECT messageID, content, timestamp, customerID
            FROM CustomerMessage
            WHERE customerID = %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (customer_id,))
        messages = cursor.fetchall()
        cursor.close()

        return jsonify(messages), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@customer_routes.route("/customers/<int:customer_id>/messages", methods=["POST"])
def create_customer_message(customer_id):
    try:
        data = request.get_json()

        required_fields = ["messageID", "content"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO CustomerMessage (messageID, content, timestamp, customerID)
            VALUES (%s, %s, NOW(), %s)
        """
        cursor.execute(
            query,
            (
                data["messageID"],
                data["content"],
                customer_id,
            ),
        )
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message created successfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500