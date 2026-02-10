import pandas as pd
import joblib
from pathlib import Path

# Load model once
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "RF_Model.joblib"

model = joblib.load(MODEL_PATH)

# Helper functions
def get_age_group(age):
    if age < 12:
        return "Child"
    elif age < 20:
        return "Teen"
    elif age < 35:
        return "YoungAdult"
    elif age < 60:
        return "Adult"
    else:
        return "Senior"


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
        

    if sex == 1:
        return "Miss" if age < 18 else "Mrs"
    return "Mr"
    
# Inference
def predict_survival(data: dict):
    """
    data keys:
    pclass, sex, age, sibsp, parch, fare, embarked, family_size, is_alone
    """

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

    df = pd.DataFrame([row])

    # Categorical features
    df["AgeGroup"] = get_age_group(data["age"])
    df["FareGroup"] = get_fare_group(data["fare"])
    df["Title"] = get_title(data["sex"], data["age"])

    df = pd.get_dummies(
        df,
        columns=["AgeGroup", "FareGroup", "Title"],
    )

    # Align with model features(from model training dataframe)
    expected_columns = list(model.feature_names_in_)

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    # Prediction 
    probability = model.predict_proba(df)[0][1]
    survived = int(probability >= 0.5)

    return survived, float(probability)
