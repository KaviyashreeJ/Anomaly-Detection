import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest

# Sample security log data
data = {
    "User": [1, 2, 3, 4, 5],
    "API_Call": [10, 20, 30, 40, 50],
    "Time": [15, 40, 70, 100, 200],
    "IP_Numeric": [300, 500, 700, 900, 1200]
}

df = pd.DataFrame(data)

# Train Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(df)

# Save the trained model
joblib.dump(model, "model.joblib")
print("✅ Model trained and saved as 'model.joblib'!")
