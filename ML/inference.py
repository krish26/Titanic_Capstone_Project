import pandas as pd
import joblib
from pathlib import Path

# Load model once
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "LR_Model.joblib"

model = joblib.load(MODEL_PATH)

# Helper functions
def get_age_group(age):
    if age < 12:
        return "Child"
    elif age < 20:
        return "Teen"
    elif age < 35:
        return "YoungAdult"
    # elif age < 60:
    #     return "Adult"
    else:
        return "Senior"


def get_fare_group(fare):
    if fare < 10:
        return "Low"
    elif fare < 30:
        return "Mid"
    # elif fare < 100:
    #     return "High"
    else:
        return "VeryHigh"
    
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

    df = pd.get_dummies(
        df,
        columns=["AgeGroup", "FareGroup"],
        # drop_first=True
    )

    #Ensure all 17 features exist
    expected_columns = list(model.feature_names_in_)

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[expected_columns]

    # Prediction 
    probability = model.predict_proba(df)[0][1]
    survived = int(probability >= 0.5)

    return survived, float(probability)
