from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
import pandas as pd
import joblib
import random
import numpy as np   # ✅ added to handle numpy arrays

sys.path.append(os.path.abspath(os.path.join('..','..')))
from config import MODELS_PIPELINES

app = FastAPI(title="MediSense AI API")

# =====================================
# CORS
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# LOAD MODELS
# =====================================
try:
    diagnosis_model = joblib.load(f"{MODELS_PIPELINES}/Disease_diagnosis_ml_pipeline.pkl")
    severity_model = joblib.load(f"{MODELS_PIPELINES}/Disease_Severity_ml_pipeline.pkl")
    treatment_model = joblib.load(f"{MODELS_PIPELINES}/Disease_Treatment_Plan_ml_pipeline.pkl")
    print("Models loaded successfully.")
except Exception as e:
    print(f"Model loading error: {e}")
    diagnosis_model = None
    severity_model = None
    treatment_model = None

# =====================================
# INPUT SCHEMA
# =====================================
class PatientData(BaseModel):
    Age: int
    Gender: str
    Symptom_1: str
    Symptom_2: str
    Symptom_3: str
    Heart_Rate_bpm: int
    Body_Temperature_C: float
    Blood_Pressure_mmHg: str
    Oxygen_Saturation_pct: int

# =====================================
# HOME
# =====================================
@app.get("/")
def home():
    return {"message": "Medical Diagnosis API Running"}

# =====================================
# PATIENT ID
# =====================================
def generate_patient_id():
    return "PAT-" + str(random.randint(100000, 999999))

# =====================================
# LABEL MAPPINGS
# =====================================
diagnosis_map = {
    0: "Bronchitis",
    1: "Cold",
    2: "Flu",
    3: "Healthy",
    4: "Pneumonia"
}

severity_map = {
    0: "Mild",
    1: "Moderate",
    2: "Severe"
}

# =====================================
# PREDICT
# =====================================
@app.post("/predict")
def predict(patient: PatientData):
    if diagnosis_model is None or severity_model is None or treatment_model is None:
        raise HTTPException(status_code=500, detail="Models not loaded.")

    try:
        patient_id = generate_patient_id()
        input_df = pd.DataFrame([patient.model_dump()])

        diagnosis_pred = diagnosis_model.predict(input_df)[0]
        severity_pred = severity_model.predict(input_df)[0]
        treatment_pred = treatment_model.predict(input_df)[0]

        # Map numeric predictions to human-readable labels
        diagnosis_label = diagnosis_map.get(diagnosis_pred, str(diagnosis_pred))
        severity_label = severity_map.get(severity_pred, str(severity_pred))

        # ✅ Convert treatment_pred into a clean Python list of strings
        if isinstance(treatment_pred, (np.ndarray, list)):
            treatment_plan = [str(item) for item in treatment_pred]
        else:
            treatment_plan = [str(treatment_pred)]

        return {
            "patient_id": patient_id,
            "diagnosis": diagnosis_label,
            "severity": severity_label,
            "treatment_plan": treatment_plan
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
