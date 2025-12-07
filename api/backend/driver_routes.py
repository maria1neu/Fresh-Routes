from flask import Blueprint, jsonify, request
from backend.db_connection import db
from mysql.connector import Error

# Blueprint for customer-facing routes
driver_routes = Blueprint("driver_routes", __name__)

#List all order for driver
@driver_routes.route("/driver/<int:driverID>/order", methods=["GET"])
def get_all_deliveries(driverID):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute(
            """
            SELECT orderID, orderDate, scheduledTime, deliveryAddress, status, driverID 
            FROM `Order` 
            WHERE driverID = %s
            """,
            (driverID,),
            )
        order_list = cursor.fetchall()
        cursor.close()

        return jsonify(order_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#Update driver order status 
@driver_routes.route("/driver/<int:driverID>/order/<int:orderID>", methods=["PUT"])
def update_order_status(driverID, orderID):
    try:
        data = request.get_json()

        allowed_fields = ["status"]
        update_fields = []
        params = []

        # Only allow updating a clear set of fields
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        # Make sure the produce exists
        cursor.execute(
            "SELECT orderID " \
            "FROM `Order` " \
            "WHERE driverID = %s AND orderID = %s",
            (driverID, orderID,),
        )
        if not cursor.fetchall():
            cursor.close()
            return jsonify({"error": "Driver entry not found"}), 404

        # executes function 
        params.append(driverID)
        params.append(orderID)
        query = f"UPDATE `Order` SET {', '.join(update_fields)} WHERE driverID = %s AND orderID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Driver updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#Log delivery issue 
@driver_routes.route("/driver/<int:orderID>/order/deliveryIssue", methods=["POST"])
def create_issue_report(orderID):
    try:
        data = request.get_json()

        required_fields = ["issueID", "timestamp", "description"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO DeliveryIssue (issueID, timestamp, description, orderID)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["issueID"],
                data['timestamp'],
                data['description'], 
                orderID,
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Issure reported succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500

# Conversaation history between driver and admin 
@driver_routes.route("/driver/<int:driverID>/deliverymessage", methods=["GET"])
def get_message(driverID):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute(
            """
            SELECT messageID, timestamp, content, driverID
            FROM DeliveryMessage
            WHERE driverID = %s
            """,
            (driverID,),
        )
        message = cursor.fetchall()
        cursor.close()

        if not message:
            return jsonify({"error": "Message not found"}), 404

        return jsonify(message), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#Send message to admin  
@driver_routes.route("/driver/<int:driverID>/deliverymessage", methods=["POST"])
def send_message(driverID):
    try:
        data = request.get_json()

        required_fields = ["messageID", "timestamp", "content"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = db.get_db().cursor()

        query = """
            INSERT INTO DeliveryMessage (messageID, timestamp, content, driverID)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                data["messageID"],
                data['timestamp'],
                data['content'], 
                driverID,
            ),
            )
        
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Message sent succesfully"}), 201

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Driver availability
@driver_routes.route("/driver/<int:driverID>/driveravailability", methods=["GET"])
def get_availability(driverID):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute(
            """SELECT availabilityID, availStartTime, availEndTime, locationZone, date, isAvailable, driverID
            FROM DriverAvailability
            WHERE driverID = %s""",
            (driverID,),
            )
        order_list = cursor.fetchall()
        cursor.close()

        return jsonify(order_list), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500

#Update driver availability days 
@driver_routes.route("/driver/<int:driverID>/driveravailability", methods=["PUT"])
def update_driver_availability(driverID):
    try:
        data = request.get_json()

        allowed_fields = ['availabilityID', 'availStartTime', 'availEndTime', 'locationZone', 'date', 'isAvailable', 'driverID']
        update_fields = []
        params = []

        # Only allow updating a clear set of fields
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                params.append(data[field])

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        cursor = db.get_db().cursor()

        cursor.execute(
            """
            SELECT availabilityID, availStartTime, availEndTime, locationZone, date, isAvailable, driverID 
            FROM DriverAvailability 
            WHERE driverID = %s
            """,
            (driverID,),
        )
        if not cursor.fetchall():
            cursor.close()
            return jsonify({"error": "Driver availability entry not found"}), 404

        # executes function 
        params.append(driverID)
        query = f"UPDATE DriverAvailability SET {', '.join(update_fields)} WHERE driverID = %s"
        cursor.execute(query, params)
        db.get_db().commit()
        cursor.close()

        return jsonify({"message": "Availability updated successfully"}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
# Trafic for driver 
@driver_routes.route("/driver/<int:driverID>/traffic", methods=["GET"])
def get_driver_route(driverID):
    try:
        cursor = db.get_db().cursor(dictionary=True)

        cursor.execute(
            """
            SELECT locationID, timestamp, trafficLevels, notification, driverID
            FROM Traffic
            WHERE driverID = %s
            """,
            (driverID,),
        )
        traffic = cursor.fetchall()
        cursor.close()

        if not traffic:
            return jsonify({"error": "No traffic records found for this driver"}), 404

        return jsonify(traffic), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500
    