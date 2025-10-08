import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

DATA_PATH = "data/identity_features.csv"
MODEL_PATH = "models/isolation_forest.pkl"
SCALER_PATH = "models/scaler.pkl"

def train():
    df = pd.read_csv(DATA_PATH)
    # Keep address column separate
    addresses = df['from']
    X = df.drop(columns=['from'])

    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    # Standardise features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Isolation Forest (contamination ~ expected % of fraud; 0.02 = 2%)
    model = IsolationForest(
        n_estimators=200,
        max_samples='auto',
        contamination=0.02,
        random_state=42
    )
    model.fit(X_scaled)

    # Save artefacts
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved → {MODEL_PATH}")

def predict_and_score():
    df = pd.read_csv(DATA_PATH)
    addresses = df['from']
    X = df.drop(columns=['from'])
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    scaler = joblib.load(SCALER_PATH)
    model = joblib.load(MODEL_PATH)

    X_scaled = scaler.transform(X)
    # IsolationForest returns -1 for outliers, 1 for normal, plus decision_function scores
    preds = model.predict(X_scaled)
    scores = model.decision_function(X_scaled)  # higher => more normal

    # Convert to 0‑100 risk score (inverse of normality)
    risk = (1 - ((scores - scores.min()) / (scores.max() - scores.min()))) * 100
    result = pd.DataFrame({
        "address": addresses,
        "risk_score": risk.round(2),
        "is_anomaly": (preds == -1).astype(int)
    })
    result = result.sort_values("risk_score", ascending=False)
    result.to_csv("data/risk_report.csv", index=False)
    print("Risk report saved → data/risk_report.csv")
    print(result.head(10))

if __name__ == "__main__":
    train()
    predict_and_score()
