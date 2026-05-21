from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)
CORS(app)

# ==========================================
# 1. AI Training Data (Intent Classification)
# ==========================================
# We teach the AI what different sentences mean
training_sentences = [
    "book a flight", "i want to fly to london", "find tickets", "search for flights", "where can i travel",
    "login to my account", "sign in", "create account", "register for an account", "i need to log in",
    "cancel my ticket", "view my flights", "show my itinerary", "pay for my ticket", "where is my flight"
]

# We label those sentences with the correct "Action"
training_labels = [
    "route_to_search", "route_to_search", "route_to_search", "route_to_search", "route_to_search",
    "route_to_login", "route_to_login", "route_to_login", "route_to_login", "route_to_login",
    "route_to_itinerary", "route_to_itinerary", "route_to_itinerary", "route_to_itinerary", "route_to_itinerary"
]

# ==========================================
# 2. Train the Machine Learning Model
# ==========================================
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(training_sentences)

classifier = MultinomialNB()
classifier.fit(X_train, training_labels)
print("✅ AI NLP Model Trained and Ready!")

# ==========================================
# 3. The REST API Endpoint (Port 5001)
# ==========================================
@app.route('/api/ai/intent', methods=['POST'])
def handle_intent():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"action": "unknown"}), 400
        
    # The AI predicts what the user wants based on its training!
    X_test = vectorizer.transform([user_message.lower()])
    prediction = classifier.predict(X_test)[0]
    
    return jsonify({
        "status": "success",
        "action": prediction,
        "original_message": user_message
    }), 200

if __name__ == '__main__':
    # Notice this runs on Port 5001, completely separate from your main database API!
    app.run(port=5001, debug=True)