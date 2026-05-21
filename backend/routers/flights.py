# routers/flights.py
from flask import Blueprint, request, jsonify

from database import db_cursor
from services import serialize_row

flights_router = Blueprint('flights', __name__)

_VALID_STATUSES = ['Scheduled', 'Delayed', 'Arrived', 'Departed', 'Canceled']


@flights_router.route('', methods=['GET'])
def search_flights():
    """
    Flight Search & Discovery Engine
    ---
    tags:
      - Flight Discovery
    parameters:
      - name: from
        in: query
        type: string
        required: true
        description: Departure IATA code (e.g., IST)
      - name: to
        in: query
        type: string
        required: true
        description: Arrival IATA code (e.g., LHR)
      - name: date
        in: query
        type: string
        required: true
        description: Departure date in YYYY-MM-DD format
    responses:
      200:
        description: Matching flights with aircraft info and seat load factor.
      400:
        description: Missing one or more required query parameters.
      500:
        description: Database error.
    """
    dep_iata    = (request.args.get('from',  '') or '').strip().upper()
    arr_iata    = (request.args.get('to',    '') or '').strip().upper()
    flight_date = (request.args.get('date',  '') or '').strip()

    if not all([dep_iata, arr_iata, flight_date]):
        return jsonify({"status": "error", "message": "'from', 'to', and 'date' parameters are required."}), 400

    try:
        rows = []
        with db_cursor() as (conn, cursor):
            cursor.execute(
                """SELECT f.flight_number,
                          f.departure_iata,
                          f.arrival_iata,
                          f.departure_time,
                          f.arrival_time,
                          f.status,
                          a.model,
                          a.seating_capacity,
                          dep.city  AS departure_city,
                          arr.city  AS arrival_city,
                          fn_load_factor(f.flight_number) AS load_factor_pct
                   FROM   flight   f
                   JOIN   aircraft a   ON a.aircraft_id = f.aircraft_id
                   JOIN   airport  dep ON dep.iata_code  = f.departure_iata
                   JOIN   airport  arr ON arr.iata_code  = f.arrival_iata
                   WHERE  f.departure_iata = %s
                     AND  f.arrival_iata   = %s
                     AND  DATE(f.departure_time) = %s
                     AND  f.status != 'Canceled'""",
                (dep_iata, arr_iata, flight_date)
            )
            rows = cursor.fetchall()

        data = [serialize_row(r) for r in rows]
        return jsonify({"status": "success", "count": len(data), "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@flights_router.route('/all', methods=['GET'])
def get_all_flights():
    """
    Retrieve All Flights
    ---
    tags:
      - Flight Discovery
    responses:
      200:
        description: Full flight list with airport and aircraft details.
      500:
        description: Database error.
    """
    try:
        rows = []
        with db_cursor() as (conn, cursor):
            cursor.execute(
                """SELECT f.flight_number,
                          f.departure_iata,
                          f.arrival_iata,
                          f.departure_time,
                          f.arrival_time,
                          f.status,
                          a.model,
                          dep.city AS departure_city,
                          arr.city AS arrival_city
                   FROM   flight   f
                   JOIN   aircraft a   ON a.aircraft_id = f.aircraft_id
                   JOIN   airport  dep ON dep.iata_code  = f.departure_iata
                   JOIN   airport  arr ON arr.iata_code  = f.arrival_iata
                   ORDER  BY f.departure_time DESC"""
            )
            rows = cursor.fetchall()

        data = [serialize_row(r) for r in rows]
        return jsonify({"status": "success", "count": len(data), "data": data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@flights_router.route('/<flight_number>/status', methods=['PATCH'])
def update_flight_status(flight_number):
    """
    Update Flight Status (Admin)
    ---
    tags:
      - Flight Discovery
    parameters:
      - name: flight_number
        in: path
        type: string
        required: true
        example: TK2601
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [status]
          properties:
            status:
              type: string
              example: Delayed
    responses:
      200:
        description: Flight status updated successfully.
      400:
        description: Invalid or missing status value.
      404:
        description: Flight not found.
      500:
        description: Database error.
    """
    data       = request.get_json(silent=True) or {}
    new_status = data.get('status', '').strip()

    if new_status not in _VALID_STATUSES:
        return jsonify({
            "status": "error",
            "message": f"Status must be one of: {_VALID_STATUSES}"
        }), 400

    try:
        flight = None
        with db_cursor() as (conn, cursor):
            cursor.execute(
                "SELECT flight_number FROM flight WHERE flight_number = %s",
                (flight_number,)
            )
            flight = cursor.fetchone()
            if flight:
                cursor.execute(
                    "UPDATE flight SET status = %s WHERE flight_number = %s",
                    (new_status, flight_number)
                )

        if not flight:
            return jsonify({"status": "error", "message": "Flight not found."}), 404

        return jsonify({
            "status":  "success",
            "message": f"Flight {flight_number} status updated to '{new_status}'."
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@flights_router.route('/report/<flight_number>', methods=['GET'])
def flight_sales_report(flight_number):
    """
    Flight Sales Report
    ---
    tags:
      - Flight Discovery
    parameters:
      - name: flight_number
        in: path
        type: string
        required: true
        example: TK1001
    responses:
      200:
        description: Revenue and booking summary via sp_flight_sales_report.
      404:
        description: Flight not found or no tickets issued.
      500:
        description: Database error.
    """
    try:
        results = []
        with db_cursor() as (conn, cursor):
            cursor.callproc('sp_flight_sales_report', [flight_number])
            for result_set in cursor.stored_results():
                results.extend(result_set.fetchall())

        if not results:
            return jsonify({
                "status":  "error",
                "message": "No report data found. The flight may not exist or has no tickets."
            }), 404

        return jsonify({"status": "success", "data": serialize_row(results[0])}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
