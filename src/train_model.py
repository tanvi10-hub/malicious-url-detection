#!/usr/bin/env python3
"""
Train and export model artifacts compatible with current environment.
"""

import os
import sys
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, "data", "features_v2.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model_v2.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")
TARGET_COLUMN = "type"


def main():
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset not found: {DATASET_PATH}")
        sys.exit(1)

    print(f"Loading dataset: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)

    if TARGET_COLUMN not in df.columns:
        print(f"Missing target column '{TARGET_COLUMN}' in dataset")
        sys.exit(1)

    df = df.dropna(subset=[TARGET_COLUMN])
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].astype(str)

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    )

    print("Training RandomForest model...")
    model.fit(X, y_encoded)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print(f"Saved model: {MODEL_PATH}")
    print(f"Saved encoder: {ENCODER_PATH}")
    print(f"Classes: {list(encoder.classes_)}")


if __name__ == "__main__":
    main()
