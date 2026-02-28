import os
import yaml
from datetime import datetime

# -------------------------------
# CONFIGURATION
# -------------------------------
CONTROLS_DIR = "controls"
BASELINE_FILE = "baseline/v1.0/baselines.yaml"
EXCEPTIONS_DIR = "exceptions/schema"

# -------------------------------
# HELPERS
# -------------------------------
def load_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_controls():
    controls = []
    for category in os.listdir(CONTROLS_DIR):
        category_path = os.path.join(CONTROLS_DIR, category)
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                if file.endswith(".yaml"):
                    ctrl = load_yaml(os.path.join(category_path, file))
                    controls.append(ctrl)
    return controls

def load_baseline():
    return load_yaml(BASELINE_FILE)["controls"]

def load_exceptions():
    exceptions = {}
    if os.path.exists(EXCEPTIONS_DIR):
        for file in os.listdir(EXCEPTIONS_DIR):
            if file.endswith(".yaml"):
                ex = load_yaml(os.path.join(EXCEPTIONS_DIR, file))
                exceptions[ex["control_id"]] = ex
    return exceptions

# -------------------------------
# CALCULATIONS
# -------------------------------
def get_compliance_value(control, exceptions):
    ctrl_id = control["id"]
    # Use exception if present
    ex = exceptions.get(ctrl_id)
    if ex:
        if ex["status"] == "Active" and datetime.strptime(ex["expiration_date"], "%Y-%m-%d") >= datetime.today():
            return 1.0
        else:
            return 0.0
    # Default compliance_value from control
    return control.get("compliance_value", 0.0)

def calculate_weighted_score(control, exceptions):
    compliance_value = get_compliance_value(control, exceptions)
    risk_weight = control.get("risk_weight", 1.0)
    weighted_score = compliance_value * risk_weight
    return weighted_score, risk_weight

def compute_composite_score(controls):
    exceptions = load_exceptions()
    total_weighted_score = 0.0
    total_risk_weight = 0.0

    for control in controls:
        w_score, r_weight = calculate_weighted_score(control, exceptions)
        total_weighted_score += w_score
        total_risk_weight += r_weight

    # Zero-weight guard condition
    if total_risk_weight == 0:
        return 0.0, "INVALID_BASELINE"

    framework_score = total_weighted_score / total_risk_weight
    return round(framework_score, 2), None

# -------------------------------
# MAIN
# -------------------------------
def main():
    print("Loading controls...")
    controls = load_controls()
    print(f"Loaded {len(controls)} controls.")
    score, error = compute_composite_score(controls)
    if error:
        print(f"Error computing score: {error}")
    else:
        print(f"Composite Framework Score: {score * 100:.2f}%")

if __name__ == "__main__":
    main()
