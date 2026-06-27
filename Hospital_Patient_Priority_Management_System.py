

class Patient:
    def __init__(self, name, age, symptoms, vital_signs, pain_level=0):
        self.name = name
        self.age = age
        self.symptoms = symptoms       # list of symptom strings
        self.vital_signs = vital_signs # dict with keys: bp, hr, spo2
        self.pain_level = pain_level   # 0 to 10
        self.priority = None

    # FIXED: Added __str__ so print(patient) shows useful info
    def __str__(self):
        return (f"Patient: {self.name} | Age: {self.age} | "
                f"Symptoms: {', '.join(self.symptoms)} | Priority: {self.priority}")


class PrioritySystem:
    def __init__(self):
        # Predefined medical rules - same as original
        self.emergency_symptoms = {
            "chest pain", "severe bleeding", "unconscious",
            "stroke", "major accident", "cardiac arrest",
            "anaphylaxis", "choking", "severe burns"
        }
        self.urgent_symptoms = {
            "fever", "fracture", "moderate pain",
            "breathing difficulty", "high fever",
            "severe headache", "vision loss"
        }

    def categorize(self, patient):
        reasons = []  # FIXED: track why priority was assigned

        # Rule 1: Check emergency symptoms
        for symptom in patient.symptoms:
            if symptom.lower() in self.emergency_symptoms:
                patient.priority = "Emergency"
                reasons.append(f"Emergency symptom: '{symptom}'")

        # Rule 2: Check urgent symptoms (only if not already Emergency)
        if patient.priority != "Emergency":
            for symptom in patient.symptoms:
                if symptom.lower() in self.urgent_symptoms:
                    patient.priority = "Urgent"
                    reasons.append(f"Urgent symptom: '{symptom}'")

        # Rule 3: Check vital signs
        # FIXED: was "elif" so vitals were SKIPPED if urgent symptoms found.
        # Now vitals can upgrade priority to Emergency even if symptoms = Urgent.
        vitals = patient.vital_signs
        if vitals.get("spo2") is not None and vitals["spo2"] < 90:
            patient.priority = "Emergency"
            reasons.append(f"SpO2 = {vitals['spo2']}% (critical, < 90%)")

        if vitals.get("hr") is not None and vitals["hr"] > 120:
            patient.priority = "Emergency"
            reasons.append(f"Heart Rate = {vitals['hr']} bpm (critical, > 120)")

        if vitals.get("bp") is not None and vitals["bp"] < 90:
            patient.priority = "Emergency"
            reasons.append(f"Blood Pressure = {vitals['bp']} mmHg (critical, < 90)")

        # Rule 4: Age factor (elderly with any symptoms)
        if patient.age > 65 and len(patient.symptoms) > 0:
            if patient.priority not in ("Emergency", "Urgent"):
                patient.priority = "Urgent"
                reasons.append(f"Elderly patient (age {patient.age}) with symptoms")

        # Rule 5: Pain level
        if patient.pain_level >= 9:
            patient.priority = "Emergency"
            reasons.append(f"Pain level {patient.pain_level}/10 (severe)")
        elif patient.pain_level >= 7:
            if patient.priority != "Emergency":
                patient.priority = "Urgent"
                reasons.append(f"Pain level {patient.pain_level}/10 (high)")

        # Default case
        if patient.priority is None:
            patient.priority = "Normal"
            reasons.append("No emergency or urgent indicators found")

        return patient.priority, reasons


def display_queue(results):
    """Display all patients sorted by priority (Emergency first)."""
    # FIXED: Added proper sorting and display function
    order = {"Emergency": 0, "Urgent": 1, "Normal": 2}
    sorted_results = sorted(results, key=lambda x: order.get(x[0].priority, 2))

    print("\n" + "=" * 60)
    print("  PATIENT PRIORITY QUEUE")
    print("=" * 60)
    for i, (patient, reasons) in enumerate(sorted_results, 1):
        symbol = {"Emergency": "🚨", "Urgent": "⚡", "Normal": "✅"}.get(patient.priority, "")
        print(f"\n  {i}. {symbol} [{patient.priority.upper()}] {patient.name} (Age: {patient.age})")
        print(f"     Symptoms : {', '.join(patient.symptoms)}")
        print(f"     Vitals   : BP={patient.vital_signs.get('bp','?')} | "
              f"HR={patient.vital_signs.get('hr','?')} | "
              f"SpO2={patient.vital_signs.get('spo2','?')}%")
        print(f"     Reasons  :")
        for r in reasons:
            print(f"       - {r}")
    print("\n" + "=" * 60)


# ─── Example Usage (same patients as original) ────────────────────────────────
if __name__ == "__main__":

    system = PrioritySystem()

    # Same 3 sample patients from original file
    patient1 = Patient(
        name="Ravi",
        age=70,
        symptoms=["fever", "breathing difficulty"],
        vital_signs={"bp": 110, "hr": 95, "spo2": 92}
    )

    patient2 = Patient(
        name="Meena",
        age=25,
        symptoms=["headache"],
        vital_signs={"bp": 120, "hr": 80, "spo2": 98}
    )

    patient3 = Patient(
        name="Arun",
        age=50,
        symptoms=["chest pain"],
        vital_signs={"bp": 85, "hr": 130, "spo2": 88}
    )

    # Assess all patients
    results = []
    for patient in [patient1, patient2, patient3]:
        priority, reasons = system.categorize(patient)
        results.append((patient, reasons))
        print(f"{patient.name} → {priority}")

    # Display sorted queue
    display_queue(results)
