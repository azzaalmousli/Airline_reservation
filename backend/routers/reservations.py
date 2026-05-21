# routers/reservations.py
from flask import Blueprint, request, jsonify

from database import db_cursor
from services import serialize_row

reservations_router = Blueprint('reservations', __name__)


@reservations_router.route('/reservations', methods=['POST'])
def book_flight():
    """
    Create Pending Flight Reservation
    ---
    tags:
      - Reservations & Passenger Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [customer_id, flight_number]
          properties:
            customer_id:
              type: integer
              example: 2
            flight_number:
              type: string
              example: TK2601
    responses:
      201:
        description: Reservation and unpaid ticket created successfully.
      400:
        description: Missing required fields.
      404:
        description: Flight not found or is Canceled.
      409:
        description: Flight is fully booked (no available seats).
      500:
        description: Database error.
    """
    data          = request.get_json(silent=True) or {}
    customer_id   = data.get('customer_id')
    flight_number = (data.get('flight_number') or '').strip()

    if not customer_id or not flight_number:
        return jsonify({"status": "error", "message": "customer_id and flight_number are required."}), 400

    try:
        error_code    = None
        error_message = None

        with db_cursor() as (conn, cursor):
            # 1. Verify the flight exists and is not Canceled
            cursor.execute(
                """SELECT f.flight_number,
                          DATE(f.departure_time) AS dep_date,
                          a.seating_capacity
                   FROM   flight   f
                   JOIN   aircraft a ON a.aircraft_id = f.aircraft_id
                   WHERE  f.flight_number = %s
                     AND  f.status != 'Canceled'""",
                (flight_number,)
            )
            flight = cursor.fetchone()

            if not flight:
                error_code    = 404
                error_message = "Flight not found or is canceled."
            else:
                # 2. Seat availability check using fn_load_factor
                cursor.execute(
                    """SELECT COUNT(tr.ticket_number) AS booked
                       FROM   reservation       r
                       JOIN   ticket_reservation tr ON tr.booking_id = r.booking_id
                       WHERE  r.flight_number = %s
                         AND  r.status != 'Canceled'""",
                    (flight_number,)
                )
                booked_row = cursor.fetchone()
                booked     = booked_row['booked'] if booked_row else 0

                if booked >= flight['seating_capacity']:
                    error_code    = 409
                    error_message = "This flight is fully booked. No seats available."
                else:
                    # 3. Use the flight's departure date as booking_date so the
                    #    trg_reservation_date_check trigger is always satisfied.
                    cursor.execute(
                        """INSERT INTO reservation
                           (customer_id, flight_number, booking_date, status)
                           VALUES (%s, %s, %s, 'Pending')""",
                        (customer_id, flight_number, flight['dep_date'])
                    )
                    booking_id = cursor.lastrowid

                    # 4. Generate a unique ticket number
                    cursor.execute("SELECT IFNULL(MAX(ticket_number), 4999) + 1 AS new_num FROM ticket")
                    new_ticket_num = cursor.fetchone()['new_num']
                    seat           = f"{new_ticket_num}A"

                    # 5. Create the unpaid ticket
                    cursor.execute(
                        """INSERT INTO ticket
                           (ticket_number, seat_number, fare_class, price, payment_status, issue_date)
                           VALUES (%s, %s, 'Economy', 300.00, 'Unpaid', NOW())""",
                        (new_ticket_num, seat)
                    )

                    # 6. Link ticket to reservation
                    cursor.execute(
                        """INSERT INTO ticket_reservation (booking_id, ticket_number, passenger_type)
                           VALUES (%s, %s, 'Adult')""",
                        (booking_id, new_ticket_num)
                    )

        if error_code:
            return jsonify({"status": "error", "message": error_message}), error_code

        return jsonify({
            "status":  "success",
            "message": "Flight booked successfully! Proceed to payment.",
            "booking_id":  booking_id,
            "ticket_number": new_ticket_num
        }), 201

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reservations_router.route('/itinerary/<int:customer_id>', methods=['GET'])
def get_itinerary(customer_id):
    """
    Fetch Customer Itinerary
    ---
    tags:
      - Reservations & Passenger Management
    parameters:
      - name: customer_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: All active bookings via sp_customer_itinerary stored procedure.
      500:
        description: Database error.
    """
    try:
        results = []
        with db_cursor() as (conn, cursor):
            cursor.callproc('sp_customer_itinerary', [customer_id])
            for result_set in cursor.stored_results():
                results.extend(result_set.fetchall())

        # Filter out soft-canceled reservations (no linked ticket data after cancel)
        active = [
            serialize_row(r) for r in results
            if r.get('reservation_status', '').lower() != 'canceled'
        ]
        return jsonify({"status": "success", "data": active}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reservations_router.route('/payments', methods=['POST'])
def process_payment():
    """
    Process Secure Ticket Payment
    ---
    tags:
      - Reservations & Passenger Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [ticket_number, amount]
          properties:
            ticket_number:
              type: integer
              example: 5001
            amount:
              type: number
              example: 300.00
    responses:
      200:
        description: Payment recorded. DB trigger auto-updates ticket payment_status.
      400:
        description: Missing ticket_number or amount.
      404:
        description: No reservation linked to this ticket.
      500:
        description: Database error.
    """
    data          = request.get_json(silent=True) or {}
    ticket_number = data.get('ticket_number')
    amount        = data.get('amount')

    if not ticket_number or not amount:
        return jsonify({"status": "error", "message": "ticket_number and amount are required."}), 400

    try:
        reservation = None
        with db_cursor() as (conn, cursor):
            cursor.execute(
                "SELECT booking_id FROM ticket_reservation WHERE ticket_number = %s",
                (ticket_number,)
            )
            reservation = cursor.fetchone()

            if reservation:
                cursor.execute(
                    """INSERT INTO payment
                       (booking_id, ticket_number, amount, payment_method, payment_date)
                       VALUES (%s, %s, %s, 'Credit Card', NOW())""",
                    (reservation['booking_id'], ticket_number, amount)
                )
                # Confirm the reservation once payment is recorded
                cursor.execute(
                    "UPDATE reservation SET status = 'Confirmed' WHERE booking_id = %s",
                    (reservation['booking_id'],)
                )

        if not reservation:
            return jsonify({"status": "error", "message": "No reservation found for this ticket."}), 404

        return jsonify({"status": "success", "message": "Payment confirmed!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@reservations_router.route('/tickets/cancel', methods=['POST'])
def cancel_ticket():
    """
    Cancel Ticket & Reservation
    ---
    tags:
      - Reservations & Passenger Management
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [ticket_number]
          properties:
            ticket_number:
              type: integer
              example: 5001
    responses:
      200:
        description: Ticket canceled. Reservation marked Canceled; seat freed.
      400:
        description: Missing ticket_number.
      404:
        description: Ticket not found.
      500:
        description: Database error.
    """
    data          = request.get_json(silent=True) or {}
    ticket_number = data.get('ticket_number')

    if not ticket_number:
        return jsonify({"status": "error", "message": "ticket_number is required."}), 400

    try:
        record = None
        with db_cursor() as (conn, cursor):
            cursor.execute(
                "SELECT booking_id FROM ticket_reservation WHERE ticket_number = %s",
                (ticket_number,)
            )
            record = cursor.fetchone()

            if record:
                booking_id = record['booking_id']

                # Delete payment records for this ticket (refund simulation)
                cursor.execute("DELETE FROM payment          WHERE ticket_number = %s", (ticket_number,))
                # Remove the ticket-to-booking link
                cursor.execute("DELETE FROM ticket_reservation WHERE ticket_number = %s", (ticket_number,))
                # Delete the physical ticket (frees the seat)
                cursor.execute("DELETE FROM ticket            WHERE ticket_number = %s", (ticket_number,))
                # Soft-cancel the reservation record (preserves booking history)
                cursor.execute(
                    "UPDATE reservation SET status = 'Canceled' WHERE booking_id = %s",
                    (booking_id,)
                )

        if not record:
            return jsonify({"status": "error", "message": "Ticket not found."}), 404

        return jsonify({"status": "success", "message": "Ticket canceled and reservation marked as Canceled."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
