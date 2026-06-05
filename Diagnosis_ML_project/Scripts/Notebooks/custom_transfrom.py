# import libraries
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin,ClassifierMixin

# =====================================
# Blood Pressure Split Function
# =====================================

def split_blood_pressure(df):

    X = df.copy()

    # Remove Patient_ID if present
    if "Patient_ID" in X.columns:
        X = X.drop(columns=["Patient_ID"])

    # Split blood pressure
    bp_split = (
        X["Blood_Pressure_mmHg"]
        .astype(str)
        .str.split("/", expand=True)
    )

    # Convert to numeric
    bp_split = bp_split.apply(
        pd.to_numeric,
        errors="coerce"
    )

    X["systolic"] = bp_split[0]
    X["diastolic"] = bp_split[1]

    return X[["systolic", "diastolic"]]


# =====================================
# Feature Names
# =====================================

def get_bp_names(
    transformer,
    input_features
):

    return [
        "systolic",
        "diastolic"
    ]




# label_decoder.py


class LabelDecoderWrapper(BaseEstimator, ClassifierMixin):
    def __init__(self, base_estimator, label_encoder):
        self.base_estimator = base_estimator
        self.label_encoder = label_encoder

    def fit(self, X, y):
        y_encoded = self.label_encoder.transform(y)
        self.base_estimator.fit(X, y_encoded)
        return self

    def predict(self, X):
        y_encoded = self.base_estimator.predict(X)
        return self.label_encoder.inverse_transform(y_encoded)

    def predict_proba(self, X):
        return self.base_estimator.predict_proba(X)
