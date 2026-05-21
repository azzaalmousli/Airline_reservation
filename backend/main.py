# main.py
import time
from decimal import Decimal
from datetime import datetime, date

from flask import Flask, g, request
from flask.json.provider import DefaultJSONProvider
from flask_cors import CORS
from flasgger import Swagger

from routers.auth import auth_router
from routers.flights import flights_router
from routers.reservations import reservations_router
from routers.ai import ai_router
from services import log_performance


# ---------------------------------------------------------------------------
# Custom JSON provider: serializes Decimal and datetime without crashing
# ---------------------------------------------------------------------------
class AeroSmartJSONProvider(DefaultJSONProvider):
    @staticmethod
    def default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, (datetime, date)):
            return str(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.json_provider_class = AeroSmartJSONProvider
app.json = AeroSmartJSONProvider(app)

CORS(app)

app.config['SWAGGER'] = {
    'title': 'AeroSmart RESTful API Engine',
    'uiversion': 3,
    'description': (
        'Phase 2 – Full Implementation. '
        'Interactive documentation for the AeroSmart Airlines REST API.'
    )
}
swagger = Swagger(app)

# ---------------------------------------------------------------------------
# Blueprint registration
# ---------------------------------------------------------------------------
app.register_blueprint(auth_router,         url_prefix='/api/auth')
app.register_blueprint(flights_router,      url_prefix='/api/flights')
app.register_blueprint(reservations_router, url_prefix='/api')
app.register_blueprint(ai_router,           url_prefix='/api/ai')


# ---------------------------------------------------------------------------
# Performance-logging middleware
# Feeds the system_performance_log table and the vw_system_stability_metrics
# / vw_cloud_infrastructure_costs database views automatically.
# ---------------------------------------------------------------------------
@app.before_request
def _start_timer():
    g.start_time = time.time()


@app.after_request
def _log_performance(response):
    if hasattr(g, 'start_time'):
        elapsed_ms = (time.time() - g.start_time) * 1000
        operation  = f"{request.method} {request.path}"
        status     = 'Success' if response.status_code < 400 else f'Failed - {response.status_code}'
        log_performance(operation, elapsed_ms, status)
    return response


# ---------------------------------------------------------------------------
# System health endpoint (uses the DB view directly)
# ---------------------------------------------------------------------------
@app.route('/api/system/health', methods=['GET'])
def system_health():
    """
    System Stability Metrics
    ---
    tags:
      - System
    responses:
      200:
        description: Aggregated performance metrics from vw_system_stability_metrics.
      500:
        description: Database error.
    """
    from database import db_cursor
    from services import serialize_row
    from flask import jsonify
    try:
        with db_cursor() as (conn, cursor):
            cursor.execute("SELECT * FROM vw_system_stability_metrics")
            rows = cursor.fetchall()
        return jsonify({"status": "success", "data": [serialize_row(r) for r in rows]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/system/costs', methods=['GET'])
def system_costs():
    """
    Cloud Infrastructure Cost Estimate
    ---
    tags:
      - System
    responses:
      200:
        description: Daily compute cost estimates from vw_cloud_infrastructure_costs.
      500:
        description: Database error.
    """
    from database import db_cursor
    from services import serialize_row
    from flask import jsonify
    try:
        with db_cursor() as (conn, cursor):
            cursor.execute("SELECT * FROM vw_cloud_infrastructure_costs ORDER BY active_date DESC")
            rows = cursor.fetchall()
        return jsonify({"status": "success", "data": [serialize_row(r) for r in rows]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("AeroSmart API (Phase 2) starting on http://127.0.0.1:5000")
    print("Swagger docs: http://127.0.0.1:5000/apidocs")
    app.run(port=5000, debug=True)
