from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ==========================================
# MODULE 1: User Authentication (Login)
# ==========================================
@app.route('/api/auth/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data.get('email')
        
        conn = mysql.connector.connect(
            host="localhost", user="root",password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Check if the user exists in the database
        cursor.execute("SELECT customer_id, name FROM customer WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            return jsonify({"status": "success", "user": user}), 200
        else:
            return jsonify({"status": "error", "message": "User not found. Please register."}), 404
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# ==========================================
# MODULE 1.5: User Registration
# ==========================================
@app.route('/api/auth/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        passport = data.get('passport')
        dob = data.get('dob')
        phone = data.get('phone')

        # Check if any field is missing
        if not all([name, email, passport, dob, phone]):
            return jsonify({"status": "error", "message": "All fields are required."}), 400

        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Insert the new customer into the database
        query = """
            INSERT INTO customer (name, email, passport_number, date_of_birth, phone_number) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, passport, dob, phone))
        conn.commit()  # Save the changes to the database
        
        # Get the ID of the user we just created
        new_id = cursor.lastrowid
        
        return jsonify({"status": "success", "user": {"customer_id": new_id, "name": name}}), 201
        
    except mysql.connector.IntegrityError:
        # This catches errors if the email, passport, or phone already exists in the DB
        return jsonify({"status": "error", "message": "Email, Passport, or Phone already registered."}), 409
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ==========================================
# MODULE 2: Flight Search & Discovery
# ==========================================
@app.route('/api/flights', methods=['GET'])
def search_flights():
    try:
        # Get URL parameters (e.g., ?from=IST&to=LHR&date=2025-01-10)
        dep_iata = request.args.get('from')
        arr_iata = request.args.get('to')
        flight_date = request.args.get('date')
        
        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Query the flight table, joining with aircraft to show capacity
        query = """
            SELECT f.flight_number, f.departure_time, f.arrival_time, f.status, a.model 
            FROM flight f
            JOIN aircraft a ON f.aircraft_id = a.aircraft_id
            WHERE f.departure_iata = %s 
                AND f.arrival_iata = %s 
                AND DATE(f.departure_time) = %s
        """
        cursor.execute(query, (dep_iata, arr_iata, flight_date))
        flights = cursor.fetchall()
        
        return jsonify({"status": "success", "data": flights}), 200
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ==========================================
# MODULE 3: Flight Booking (Reservation) - UPDATED
# ==========================================
@app.route('/api/reservations', methods=['POST'])
def book_flight():
    try:
        data = request.json
        customer_id = data.get('customer_id')
        flight_number = data.get('flight_number')
        
        if not customer_id or not flight_number:
            return jsonify({"status": "error", "message": "Missing customer ID or flight number"}), 400
            
        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True)
        
        # 1. Create the Pending Reservation
        cursor.execute("""
            INSERT INTO reservation (customer_id, flight_number, booking_date, status) 
            VALUES (%s, %s, CURDATE(), 'Pending')
        """, (customer_id, flight_number))
        
        # Grab the auto-incremented booking_id
        booking_id = cursor.lastrowid 
        
        # 2. Generate a unique ticket number
        cursor.execute("SELECT MAX(ticket_number) AS max_t FROM ticket")
        max_ticket = cursor.fetchone()['max_t']
        new_ticket_num = max_ticket + 1 if max_ticket else 5000
        
        # 3. Create the Unpaid Ticket 
        # FIX: We now use the unique ticket number to guarantee the seat is never duplicated!
        seat = str(new_ticket_num) + "A" 
        
        cursor.execute("""
            INSERT INTO ticket (ticket_number, seat_number, fare_class, price, payment_status, issue_date) 
            VALUES (%s, %s, 'Economy', 300.00, 'Unpaid', NOW())
        """, (new_ticket_num, seat))
        
        # 4. Link the ticket to the reservation
        cursor.execute("""
            INSERT INTO ticket_reservation (booking_id, ticket_number, passenger_type) 
            VALUES (%s, %s, 'Adult')
        """, (booking_id, new_ticket_num))
        
        # Commit the transaction to the database
        conn.commit()
        
        return jsonify({"status": "success", "message": "Flight booked successfully!"}), 201
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# ==========================================
# MODULE 4: Fetch Itinerary
# ==========================================
@app.route('/api/itinerary/<int:customer_id>', methods=['GET'])
def get_itinerary(customer_id):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True)
        
        # Execute the stored procedure from Phase 1
        cursor.callproc('sp_customer_itinerary', [customer_id])
        
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
            
        return jsonify({"status": "success", "data": results}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()



# ==========================================
# MODULE 5: Process Payment (FINAL UPDATE)
# ==========================================
@app.route('/api/payments', methods=['POST'])
def process_payment():
    try:
        data = request.json
        ticket_number = data.get('ticket_number')
        amount = data.get('amount')
        
        if not ticket_number or not amount:
            return jsonify({"status": "error", "message": "Missing ticket details."}), 400
            
        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True) 
        
        # 1. Look up the booking_id for this specific ticket
        cursor.execute("SELECT booking_id FROM ticket_reservation WHERE ticket_number = %s", (ticket_number,))
        reservation = cursor.fetchone()
        
        if not reservation:
            return jsonify({"status": "error", "message": "Could not find reservation for this ticket."}), 404
            
        booking_id = reservation['booking_id']
        
        # 2. Insert the payment WITH booking_id AND payment_method ('Credit Card')!
        cursor.execute("""
            INSERT INTO payment (booking_id, ticket_number, amount, payment_method, payment_date) 
            VALUES (%s, %s, %s, %s, NOW())
        """, (booking_id, ticket_number, amount, 'Credit Card'))
        
        conn.commit()
        
        return jsonify({"status": "success", "message": "Payment confirmed!"}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


# ==========================================
# MODULE 6: Cancel Ticket (FINAL UPDATE)
# ==========================================
@app.route('/api/tickets/cancel', methods=['POST'])
def cancel_ticket():
    try:
        data = request.json
        ticket_number = data.get('ticket_number')
        
        conn = mysql.connector.connect(
            host="localhost", user="root", password="root", database="airline_reservation"
        )
        cursor = conn.cursor(dictionary=True) 
        
        # 1. Find the booking ID folder associated with this ticket
        cursor.execute("SELECT booking_id FROM ticket_reservation WHERE ticket_number = %s", (ticket_number,))
        reservation_record = cursor.fetchone()
        
        if reservation_record:
            booking_id = reservation_record['booking_id']
            
            # NEW: 2. Delete the Payment receipt FIRST (to satisfy the database bouncer!)
            cursor.execute("DELETE FROM payment WHERE ticket_number = %s", (ticket_number,))
            
            # 3. Delete the linking record
            cursor.execute("DELETE FROM ticket_reservation WHERE ticket_number = %s", (ticket_number,))
            
            # 4. Delete the actual ticket to free up the seat
            cursor.execute("DELETE FROM ticket WHERE ticket_number = %s", (ticket_number,))
            
            # 5. Delete the empty reservation folder
            cursor.execute("DELETE FROM reservation WHERE booking_id = %s", (booking_id,))
            
        conn.commit()
        
        return jsonify({"status": "success", "message": "Ticket, payment, and reservation completely cancelled."}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(port=5000, debug=True)