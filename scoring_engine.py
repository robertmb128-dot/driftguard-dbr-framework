import os
import yaml
from datetime import datetime

# Terminal color codes for Windows (works in most modern terminals)
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

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
    ex = exceptions.get(ctrl_id)
    if ex:
        if ex["status"] == "Active" and datetime.strptime(ex["expiration_date"], "%Y-%m-%d") >= datetime.today():
            return 1.0, True  # Active exception
        else:
            return 0.0, True  # Expired exception
    return control.get("compliance_value", 0.0), False

def calculate_weighted_score(control, exceptions):
    compliance_value, exception_applied = get_compliance_value(control, exceptions)
    risk_weight = control.get("risk_weight", 1.0)
    weighted_score = compliance_value * risk_weight
    return weighted_score, risk_weight, compliance_value, exception_applied

def compute_composite_score(controls):
    exceptions = load_exceptions()
    total_weighted_score = 0.0
    total_risk_weight = 0.0
    details = []

    for control in controls:
        w_score, r_weight, compliance_value, exception_applied = calculate_weighted_score(control, exceptions)
        total_weighted_score += w_score
        total_risk_weight += r_weight
        details.append({
            "id": control["id"],
            "name": control.get("name", ""),
            "risk_weight": r_weight,
            "compliance_value": compliance_value,
            "weighted_score": w_score,
            "exception_applied": exception_applied
        })

    if total_risk_weight == 0:
        return 0.0, "INVALID_BASELINE", details

    framework_score = total_weighted_score / total_risk_weight
    return round(framework_score, 2), None, details

# -------------------------------
# MAIN
# -------------------------------
def colorize_score(score):
    if score >= 0.9:
        return Colors.GREEN
    elif score >= 0.5:
        return Colors.YELLOW
    else:
        return Colors.RED

def main():
    print("Loading controls...")
    controls = load_controls()
    print(f"Loaded {len(controls)} controls.\n")

    score, error, details = compute_composite_score(controls)

    print("Control Scores:")
    print(f"{'ID':<10} {'Compliance':<10} {'RiskWeight':<10} {'WeightedScore':<13} {'Exception'}")
    print("-" * 60)
    for d in details:
        ex_flag = "Yes" if d["exception_applied"] else "No"
        color = Colors.GREEN if d["compliance_value"] == 1 else (Colors.YELLOW if d["compliance_value"] == 0.5 else Colors.RED)
        print(f"{d['id']:<10} {color}{d['compliance_value']:<10}{Colors.RESET} {d['risk_weight']:<10} {d['weighted_score']:<13} {ex_flag}")

    print("\nComposite Framework Score:")
    if error:
        print(f"Error: {error}")
    else:
        color = colorize_score(score)
        print(f"{color}{score * 100:.2f}%{Colors.RESET}")

    input("\nPress ENTER to exit...")  # Keeps window open

if __name__ == "__main__":
    main()
