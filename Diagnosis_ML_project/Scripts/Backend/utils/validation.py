def validate_input(data):
    required_fields = [
        "patient_name",
        "Age",
        "Symptom_1",
        "Symptom_2",
        "Symptom_3",
        "Heart_Rate_bpm",
        "Body_Temperature_C",
        "sOxygen_Saturation_%",
        "Blood_Pressure_mmH"
    ]
    for field in required_fields:
        if field not in data or data[field] =="":
            return f"{field} is required"
        return None
    
def make_predictions(processed_data,diagnosis_model,severity_model,treatment_plan_model):
    diagnosis = diagnosis_model.predict(processed_data)[0]
    severity = severity_model.predict(processed_data)[0]
    treatment_plan = treatment_plan_model.predict(processed_data)[0]
    return diagnosis,severity,treatment_plan