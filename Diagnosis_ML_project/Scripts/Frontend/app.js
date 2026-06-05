// ============================================
// API URL
// ============================================

const API_URL = "http://127.0.0.1:8000/predict";

// ============================================
// Elements
// ============================================

const form = document.getElementById(
    "predictionForm"
);

const results = document.getElementById(
    "results"
);

const themeBtn = document.getElementById(
    "themeToggle"
);

// ============================================
// Splash Screen Animation
// ============================================

window.addEventListener(
    "load",
    () => {

        const splash =
            document.getElementById(
                "splash-screen"
            );

        setTimeout(() => {

            splash.classList.add(
                "fade-out"
            );

        }, 2500);

    }
);

// ============================================
// Dark Mode Toggle
// ============================================

themeBtn.addEventListener(
    "click",
    () => {

        document.body.classList.toggle(
            "dark"
        );

        if (
            document.body.classList.contains(
                "dark"
            )
        ) {

            themeBtn.innerHTML =
                "☀️ Light Mode";

        }
        else {

            themeBtn.innerHTML =
                "🌙 Dark Mode";

        }

    }
);

// ============================================
// Scroll To Form
// ============================================

function scrollToForm() {

    document
        .getElementById(
            "formSection"
        )
        .scrollIntoView({

            behavior: "smooth"

        });

}

// ============================================
// Severity Badge Color
// ============================================

function getSeverityClass(
    severity
) {

    const value =
        severity.toLowerCase();

    if (
        value.includes("mild") ||
        value.includes("low")
    ) {

        return "success";

    }

    if (
        value.includes("moderate")
    ) {

        return "warning";

    }

    return "danger";

}

// ============================================
// Form Submission
// ============================================

form.addEventListener(
    "submit",

    async (e) => {

        e.preventDefault();

        // ====================================
        // Loading Screen
        // ====================================

        results.innerHTML = `

        <div class="placeholder">

            <div class="loader"></div>

            <h3>
                MediSense AI Analysis Running
            </h3>

            <p>
                Diagnosis Model
                • Severity Model
                • Treatment Model
            </p>

        </div>

        `;

        try {
    // ====================================
    // Collect Inputs
    // ====================================
    const patientName = document.getElementById("patientName").value;

    const data = {
        Age: Number(document.getElementById("Age").value),
        Gender: document.getElementById("Gender").value,
        Symptom_1: document.getElementById("Symptom_1").value,
        Symptom_2: document.getElementById("Symptom_2").value,
        Symptom_3: document.getElementById("Symptom_3").value,
        Heart_Rate_bpm: Number(document.getElementById("Heart_Rate_bpm").value),
        Body_Temperature_C: Number(document.getElementById("Body_Temperature_C").value),
        Blood_Pressure_mmHg: document.getElementById("Blood_Pressure_mmHg").value,
        Oxygen_Saturation_pct: Number(document.getElementById("Oxygen_Saturation_pct").value)
    };

    // ====================================
    // Validation (realistic ranges)
    // ====================================
    if (data.Age < 1 || data.Age > 100) {
        throw new Error("Age must be between 1 and 100 years.");
    }
    if (data.Heart_Rate_bpm < 40 || data.Heart_Rate_bpm > 200) {
        throw new Error("Heart Rate must be between 40 and 200 bpm.");
    }
    if (data.Body_Temperature_C < 35 || data.Body_Temperature_C > 42) {
        throw new Error("Body Temperature must be between 35°C and 42°C.");
    }
    if (data.Oxygen_Saturation_pct < 70 || data.Oxygen_Saturation_pct > 100) {
        throw new Error("Oxygen Saturation must be between 70% and 100%.");
    }

    const bpMatch = data.Blood_Pressure_mmHg.match(/^(\d{2,3})\/(\d{2,3})$/);
    if (!bpMatch) {
        throw new Error("Blood Pressure must be in format 120/80.");
    }
    const systolic = Number(bpMatch[1]);
    const diastolic = Number(bpMatch[2]);
    if (systolic < 80 || systolic > 200 || diastolic < 50 || diastolic > 120) {
        throw new Error("Blood Pressure must be within realistic range (80–200 / 50–120).");
    }

    // ====================================
    // API Request
    // ====================================
    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    // ====================================
    // Handle Error
    // ====================================
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Prediction Failed");
    }

    const result = await response.json();

    // ====================================
    // Severity Badge
    // ====================================
    const severityClass = getSeverityClass(result.severity);

    // ====================================
    // Show Result
    // ====================================
    results.innerHTML = `
        <div class="result-card">
            <div class="result-item"><h4>Patient Name</h4><div class="result-value">${patientName}</div></div>
            <div class="result-item"><h4>Patient ID</h4><div class="result-value">${result.patient_id}</div></div>
            <div class="result-item"><h4>Age</h4><div class="result-value">${data.Age}</div></div>
            <div class="result-item"><h4>Gender</h4><div class="result-value">${data.Gender}</div></div>
            <div class="result-item"><h4>Diagnosis</h4><div class="result-value">${result.diagnosis}</div></div>
            <div class="result-item"><h4>Severity</h4><span class="badge ${severityClass}">${result.severity}</span></div>
            <div class="result-item"><h4>Treatment Plan</h4><div class="result-value">${result.treatment_plan}</div></div>
        </div>
    `;
} catch (error) {
    console.error(error);
    results.innerHTML = `
        <div class="result-card">
            <div class="result-item">
                <h4>Prediction Error</h4>
                <div class="result-value">${error.message}</div>
            </div>
        </div>
    `;
}

});
