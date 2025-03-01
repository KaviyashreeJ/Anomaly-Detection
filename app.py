from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os
import joblib

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")

# Ensure model file exists
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("❌ model.joblib not found! Ensure it is uploaded.")

# Load trained model
model = joblib.load(MODEL_PATH)

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Anomaly Detection API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON data
        data = request.get_json()
        df = pd.DataFrame(data)

        # Ensure required fields exist
        required_columns = ["User", "API_Call", "Time", "IP_Numeric"]
        for col in required_columns:
            if col not in df.columns:
                return jsonify({"error": f"Missing required field: {col}"}), 400

        # Predict anomalies
        predictions = model.predict(df)
        df["Anomaly"] = ["Suspicious" if pred == -1 else "Normal" for pred in predictions]

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask API is running on Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns a port dynamically
    app.run(host="0.0.0.0", port=port)
