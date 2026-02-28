import os
import yaml
from datetime import datetime

# -----------------------------
# Configuration: Paths
# -----------------------------
CONTROLS_DIR = os.path.join("controls")
BASELINE_FILE = os.path.join("baseline", "v1.0", "baselines.yaml")
EXCEPTIONS_DIR = os.path.join("exceptions")  # Optional if you handle exceptions

# -----------------------------
# Risk Classification
# -----------------------------
RISK_LEVELS = [
    (90, 100, "Excellent"),
    (75, 89, "Good"),
    (50, 74, "Moderate"),
    (25, 49, "High Risk"),
    (0, 24, "Critical Risk"),
]

# -----------------------------
# Load YAML helper
# -----------------------------
def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# -----------------------------
# Load all controls from directories
# -----------------------------
def load_controls(controls_dir):
    controls = []
    for category in os.listdir(controls_dir):
        category_path = os.path.join(controls_dir, category)
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                if file.endswith(".yaml"):
                    control = load_yaml(os.path.join(category_path, file))
                    controls.append(control)
    return controls

# -----------------------------
# Calculate weighted control score
# -----------------------------
def calculate_weighted_score(control):
    # Compliance value: 1.0 = fully compliant, 0.5 = partial, 0.0 = non-compliant
    compliance_value = control.get("compliance_value", 0.0)
    
    # Check exception override
    if control.get("status") == "Active":
        expiration_date = control.get("expiration_date")
        if expiration_date:
            exp = datetime.strptime(expiration_date, "%Y-%m-%d").date()
            if exp >= datetime.today().date():
                compliance_value = 1.0
            else:
                compliance_value = 0.0
    
    risk_weight = control.get("risk_weight", 1.0)
    return compliance_value * risk_weight, risk_weight

# -----------------------------
# Composite score computation
# -----------------------------
def compute_composite_score(controls):
    total_weighted_score = 0.0
    total_risk_weight = 0.0
    
    for control in controls:
        w_score, r_weight = calculate_weighted_score(control)
        total_weighted_score += w_score
        total_risk_weight += r_weight

    # Guard against zero-weight baseline
    if total_risk_weight == 0:
        raise ValueError("INVALID_BASELINE: Total risk weight is zero")
    
    score = total_weighted_score / total_risk_weight
    return round(score * 100, 2)  # percentage

# -----------------------------
# Risk classification
# -----------------------------
def classify_risk(score):
    for low, high, level in RISK_LEVELS:
        if low <= score <= high:
            return level
    return "Unknown"

# -----------------------------
# Main Execution
# -----------------------------
def main():
    print("Loading controls...")
    controls = load_controls(CONTROLS_DIR)

    # Optionally override compliance values from baseline file
    if os.path.exists(BASELINE_FILE):
        baseline_data = load_yaml(BASELINE_FILE)
        baseline_controls = {c["id"]: c for c in baseline_data.get("controls", [])}
        for control in controls:
            if control["id"] in baseline_controls:
                control.update(baseline_controls[control["id"]])

    print(f"Calculating composite score for {len(controls)} controls...")
    score = compute_composite_score(controls)
    risk_level = classify_risk(score)
    
    print(f"\nComposite Environment Score: {score}%")
    print(f"Risk Classification: {risk_level}")

if __name__ == "__main__":
    main()
