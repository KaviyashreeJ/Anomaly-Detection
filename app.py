from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os

# Get the absolute path to the model file
BASE_DIR = os.path.dirname(os.path.abspath("C:/Cloud Storage and Security/Security Model/flask-anomaly-detection/app.py"))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")

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
