import pandas as pd
def prepare_input(data,patient_id):
    df = pd.DataFrame([{
        "Patient_ID":patient_id,
        "Age":data["Age"],
        "Gender":data["Gender"],
        "Symptom_1":data["Symptom_1"],
        "Symptom_2":data["Symptom_2"],
        "Symptom_3":data["Symptom_3"],
        "Heart_Rate_bpm":data["Heart_Rate_bpm"],
        "Body_Temperature_C":data["Body_Temperature_C"],
        "Blood_Pressure_mmH":data["Blood_Pressure_mmH"],
        "Oxygen_Saturation_%":data["Oxygen_Saturation_%"]
    }])
    return df