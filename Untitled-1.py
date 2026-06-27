# Simple Console-Based Patient Triage
# Fixed version of Untitled-1.py — same concept, bugs corrected

# ─── CORRECTIONS MADE ────────────────────────────────────────────────────────
# 1. bp = int(input()) — FIXED: if user enters decimal like 119.5, int() crashes.
#    Changed to float() then int conversion.
# 2. Vital sign checks were AFTER symptom checks using elif, so if a patient
#    had "fever" (Urgent), critical vitals (spo2 < 90) were NEVER checked.
#    FIXED: vital signs are now always checked separately.
# 3. No input validation — if user presses Enter without typing, program crashed.
#    FIXED: Added try/except for all numeric inputs.
# 4. symptoms was checked with "in" on a plain string — so typing "severe pain"
#    would also match "moderate pain" partially. FIXED: split by comma into list.
# 5. Added proper output with action message, not just the category name.
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 50)
print("  HOSPITAL PATIENT TRIAGE SYSTEM")
print("=" * 50)

# Get patient details
name = input("\nPatient Name: ").strip()
if name == "":
    name = "Unknown"

# FIXED: was int(input()) — crashes on non-numeric input
try:
    age = int(input("Age: "))
except ValueError:
    print("Invalid age entered. Setting age to 0.")
    age = 0

# FIXED: symptoms now split into a list for proper matching
symptoms_input = input("Symptoms (separate by comma): ").lower()
symptoms = [s.strip() for s in symptoms_input.split(",") if s.strip() != ""]

# FIXED: using float() instead of int() to avoid crash on decimal values
try:
    bp = float(input("Blood Pressure - Systolic (mmHg): "))
except ValueError:
    bp = None
    print("BP not entered, skipping.")

try:
    hr = float(input("Heart Rate (bpm): "))
except ValueError:
    hr = None
    print("HR not entered, skipping.")

try:
    spo2 = float(input("SpO2 - Oxygen Saturation (%): "))
except ValueError:
    spo2 = None
    print("SpO2 not entered, skipping.")

# ─── PRIORITY LOGIC ───────────────────────────────────────────────────────────

emergency_symptoms = [
    "chest pain", "severe bleeding", "unconscious",
    "stroke", "major accident", "major cuts",
    "cardiac arrest", "anaphylaxis", "choking"
]

urgent_symptoms = [
    "fever", "fracture", "moderate pain",
    "breathing difficulty", "high fever",
    "severe headache", "vision loss"
]

priority = "Normal"
reasons = []

# Rule 1: Emergency symptoms
for s in symptoms:
    if s in emergency_symptoms:
        priority = "Emergency"
        reasons.append(f"Symptom '{s}' is an emergency indicator")

# Rule 2: Urgent symptoms
# FIXED: was elif — now separate so it runs even with emergency symptoms
for s in symptoms:
    if s in urgent_symptoms and priority != "Emergency":
        priority = "Urgent"
        reasons.append(f"Symptom '{s}' is an urgent indicator")

# Rule 3: Vital signs — FIXED: was elif, now always checked
# This means critical vitals can upgrade even an "Urgent" to "Emergency"
if spo2 is not None and spo2 < 90:
    priority = "Emergency"
    reasons.append(f"SpO2 = {spo2}% is critically low (< 90%)")

if hr is not None and hr > 120:
    priority = "Emergency"
    reasons.append(f"Heart Rate = {hr} bpm is critically high (> 120)")

if bp is not None and bp < 90:
    priority = "Emergency"
    reasons.append(f"Blood Pressure = {bp} mmHg is critically low (< 90)")

# Rule 4: Age factor
if age > 65 and len(symptoms) > 0 and priority == "Normal":
    priority = "Urgent"
    reasons.append(f"Elderly patient (age {age}) with symptoms needs attention")

if not reasons:
    reasons.append("No critical symptoms or vital sign abnormalities detected")

# ─── OUTPUT ───────────────────────────────────────────────────────────────────

action = ""
wait = ""
if priority == "Emergency":
    action = "Send to Emergency Room IMMEDIATELY. Alert doctor NOW."
    wait = "Must be seen within 5 minutes!"
elif priority == "Urgent":
    action = "Inform doctor soon. Monitor vitals every 15 minutes."
    wait = "Must be seen within 30 minutes."
else:
    action = "Patient can wait. Nurse to check every 60 minutes."
    wait = "Can be seen within 2 hours."

print("\n" + "=" * 50)
print(f"  RESULT FOR: {name}")
print("=" * 50)
print(f"  Priority : {priority.upper()}")
print(f"  Action   : {action}")
print(f"  Wait     : {wait}")
print(f"  Reasons  :")
for r in reasons:
    print(f"    - {r}")
print("=" * 50)
