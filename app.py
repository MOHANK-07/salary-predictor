import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load models once at startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "salary_model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

FEATURES = [
    "cgpa", "college_tier", "python_skill", "dsa_skill",
    "ml_skill", "web_dev_skill", "communication_score",
    "aptitude_score", "internships", "projects",
    "backlogs", "resume_score"
]

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Salary Prediction API is running."})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        # Validate all features present
        missing = [f for f in FEATURES if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # Build input vector in correct order
        input_vector = np.array([[data[f] for f in FEATURES]])

        # Scale and predict
        input_scaled = scaler.transform(input_vector)
        predicted = model.predict(input_scaled)[0]

        # Clip to valid range (same as training)
        predicted = float(np.clip(predicted, 3, 35))

        return jsonify({
            "predicted_salary_lpa": round(predicted, 2),
            "input_received": {f: data[f] for f in FEATURES}
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
