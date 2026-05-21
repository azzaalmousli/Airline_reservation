# routers/ai.py
from flask import Blueprint, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

ai_router = Blueprint('ai', __name__)

# ---------------------------------------------------------------------------
# Training corpus – expanded for better real-world coverage
# ---------------------------------------------------------------------------
_SENTENCES = [
    # flight search
    "book a flight", "i want to fly to london", "find tickets", "search for flights",
    "where can i travel", "show me available flights", "what flights go to paris",
    "i need a ticket to dubai", "flights from istanbul to new york",
    # login / register
    "login to my account", "sign in", "create account", "register for an account",
    "i need to log in", "new user registration", "i forgot my password",
    "how do i sign up", "create a new profile",
    # itinerary / cancel / pay
    "cancel my ticket", "view my flights", "show my itinerary", "pay for my ticket",
    "where is my flight", "check my booking", "my reservations", "i want to cancel",
    "i need to pay", "show my upcoming trips", "manage my bookings",
]

_LABELS = [
    "route_to_search", "route_to_search", "route_to_search", "route_to_search",
    "route_to_search", "route_to_search", "route_to_search", "route_to_search",
    "route_to_search",
    "route_to_login", "route_to_login", "route_to_login", "route_to_login",
    "route_to_login", "route_to_login", "route_to_login", "route_to_login",
    "route_to_login",
    "route_to_itinerary", "route_to_itinerary", "route_to_itinerary",
    "route_to_itinerary", "route_to_itinerary", "route_to_itinerary",
    "route_to_itinerary", "route_to_itinerary", "route_to_itinerary",
    "route_to_itinerary", "route_to_itinerary",  # 11 itinerary sentences
]

_vectorizer  = CountVectorizer()
_X_train     = _vectorizer.fit_transform(_SENTENCES)
_classifier  = MultinomialNB()
_classifier.fit(_X_train, _LABELS)


@ai_router.route('/intent', methods=['POST'])
def handle_intent():
    """
    NLP Intent Classification Gateway
    ---
    tags:
      - AI Assistant
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [message]
          properties:
            message:
              type: string
              example: I want to fly to London next month
    responses:
      200:
        description: Predicted UI route action based on Naive Bayes classification.
      400:
        description: Missing or empty message field.
    """
    data    = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()

    if not message:
        return jsonify({"status": "error", "action": "unknown", "message": "No message provided."}), 400

    X_test     = _vectorizer.transform([message.lower()])
    prediction = _classifier.predict(X_test)[0]
    confidence = float(_classifier.predict_proba(X_test).max())

    return jsonify({
        "status":           "success",
        "action":           prediction,
        "confidence":       round(confidence, 3),
        "original_message": message
    }), 200
