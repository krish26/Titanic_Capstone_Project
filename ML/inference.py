import pandas as pd
import joblib
from pathlib import Path

"""
Pure ML inference layer.

Receives raw passenger features,
performs feature engineering,
returns prediction + probability.
"""

# Load model once
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "RF_Model.joblib"
FEATURES_PATH = BASE_DIR / "models" / "feature_cols.pkl"

# Load trained Random Forest model
model = joblib.load(MODEL_PATH)

# Load expected feature column structure from training pipeline
feature_columns = joblib.load(FEATURES_PATH)

# Helper functions
# Convert raw age into categorical age group
def get_age_group(age):
    if age < 12:
        return "Child"
    elif age < 18:
        return "Teen"
    elif age < 35:
        return "YoungAdult"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"

# Map fare value into training-based fare bins
def get_fare_group(fare):
    """
    Assign FareGroup based on the original training data distribution.
    Thresholds are derived from the min/max values of Fare within each
    FareGroup used during model training to avoid training–inference skew.
    """
    if fare <= 7.8958:
        return "Low"
    elif fare <= 14.4542:
        return "Mid"
    elif fare <= 31.0:
        return "High"
    else:
        return "VeryHigh"
    
# Generate passenger title based on sex and age 
def get_title(sex: int, age: float):
    """
    sex: 0 = male, 1 = female
    """
    if sex == 0:
        if age < 12:
            return "Master"
        else:
            return "Mr"
    else:
        if age < 18:
           return "Miss"
        else:
            return "Mrs"
 
# Feature engineering (runtime)
# Derive additional features required by the ML model
def engineer_features(data: dict) -> dict:
    family_size = data["sibsp"] + data["parch"] + 1
    is_alone = family_size == 1

    enriched = data.copy()
    enriched["family_size"] = family_size
    enriched["is_alone"] = is_alone

    return enriched

# Predict passenger survival using the trained ML model.
# Input: raw passenger features
# Output: survival prediction + probability
def predict_survival(data: dict):
    
    data = engineer_features(data)

    """
    data keys:
    pclass, sex, age, sibsp, parch, fare, embarked, family_size, is_alone
    """
    required = [
        "pclass",
        "sex",
        "age",
        "sibsp",
        "parch",
        "fare",
        "embarked",
        "family_size",
        "is_alone",
    ]

    # Validate required model inputs
    for key in required:
        if key not in data:
            raise ValueError(f"Missing field: {key}")

    # Convert user input into model-compatible feature format
    row = {
        "Pclass": data["pclass"],
        "Sex": data["sex"],
        "Age": data["age"],
        "SibSp": data["sibsp"],
        "Parch": data["parch"],
        "Fare": data["fare"],
        "Embarked": data["embarked"],
        "HasCabin": 0,  # we do not collect cabin info
        "FamilySize": data["family_size"],
        "IsAlone": int(data["is_alone"]),
    }

    # DataFrame creation
    df = pd.DataFrame([row])

    # Categorical features (recreate categorical engineered features used during training)
    df["AgeGroup"] = get_age_group(data["age"])
    df["FareGroup"] = get_fare_group(data["fare"])
    df["Title"] = get_title(data["sex"], data["age"])

    # One-hot encoding (convert categorical features into numeric representation)
    df = pd.get_dummies(
        df,
        columns=["AgeGroup", "FareGroup", "Title"],
    )

    # Align with model features(from training pipeline)
    expected_columns = feature_columns

    # Ensure inference dataframe matches training feature structure
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    # Get survival probability and convert it to binary prediction
    probability = model.predict_proba(df)[0][1]
    survived = int(probability >= 0.5)

    return survived, float(probability)
