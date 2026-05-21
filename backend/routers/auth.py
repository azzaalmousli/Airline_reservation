# routers/auth.py
import mysql.connector
from flask import Blueprint, request, jsonify

from database import db_cursor

auth_router = Blueprint('auth', __name__)


@auth_router.route('/login', methods=['POST'])
def login_user():
    """
    User Authentication Gateway
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [email]
          properties:
            email:
              type: string
              example: ahmed.ali@example.com
    responses:
      200:
        description: Authentication successful; user profile returned.
      400:
        description: Missing email field.
      404:
        description: Email not found in the database.
      500:
        description: Internal server error.
    """
    data  = request.get_json(silent=True) or {}
    email = data.get('email', '').strip()

    if not email:
        return jsonify({"status": "error", "message": "Email is required."}), 400

    try:
        user = None
        with db_cursor() as (conn, cursor):
            cursor.execute(
                "SELECT customer_id, name FROM customer WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", "user": user}), 200
        return jsonify({"status": "error", "message": "User not found."}), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@auth_router.route('/register', methods=['POST'])
def register_user():
    """
    New Passenger Registration
    ---
    tags:
      - Authentication
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [name, email, passport, dob, phone]
          properties:
            name:
              type: string
              example: Zaina Al-Mousli
            email:
              type: string
              example: zaina.m@example.com
            passport:
              type: string
              example: TR9876543
            dob:
              type: string
              example: "2004-05-18"
            phone:
              type: string
              example: "+905551234567"
    responses:
      201:
        description: Passenger registered and profile created.
      400:
        description: One or more required fields are missing.
      409:
        description: Email, passport number, or phone already registered.
      500:
        description: Internal server error.
    """
    data     = request.get_json(silent=True) or {}
    name     = data.get('name',     '').strip()
    email    = data.get('email',    '').strip()
    passport = data.get('passport', '').strip()
    dob      = data.get('dob',      '').strip()
    phone    = data.get('phone',    '').strip()

    if not all([name, email, passport, dob, phone]):
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    try:
        new_id = None
        with db_cursor() as (conn, cursor):
            cursor.execute(
                """INSERT INTO customer
                   (name, email, passport_number, date_of_birth, phone_number)
                   VALUES (%s, %s, %s, %s, %s)""",
                (name, email, passport, dob, phone)
            )
            new_id = cursor.lastrowid

        return jsonify({"status": "success", "user": {"customer_id": new_id, "name": name}}), 201

    except mysql.connector.IntegrityError:
        return jsonify({"status": "error", "message": "Email, Passport, or Phone already registered."}), 409
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
