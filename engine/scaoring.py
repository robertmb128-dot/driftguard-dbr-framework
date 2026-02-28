import yaml
import json
import sys
from pathlib import Path

VALID_COMPLIANCE_VALUES = {0.0, 0.5, 1.0}


def load_baseline(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_compliance(path):
    with open(path, "r") as f:
        return json.load(f)


def classify(score_percent):
    if 90 <= score_percent <= 100:
        return "Excellent"
    elif 75 <= score_percent < 90:
        return "Good"
    elif 50 <= score_percent < 75:
        return "Moderate"
    elif 25 <= score_percent < 50:
        return "High Risk"
    else:
        return "Critical Risk"


def main():
    if len(sys.argv) != 3:
        print("Usage: python scoring.py <baseline.yaml> <compliance.json>")
        sys.exit(1)

    baseline_path = Path(sys.argv[1])
    compliance_path = Path(sys.argv[2])

    baseline = load_baseline(baseline_path)
    compliance = load_compliance(compliance_path)

    controls = baseline.get("controls", [])

    S = 0.0
    W = 0.0

    for control in controls:
        if control.get("status") != "Active":
            continue

        control_id = control["id"]
        risk_weight = float(control["risk_weight"])

        W += risk_weight

        if control_id not in compliance:
            compliance_value = 0.0
        else:
            compliance_value = float(compliance[control_id])

            if compliance_value not in VALID_COMPLIANCE_VALUES:
                raise ValueError(
                    f"Invalid compliance value for {control_id}: {compliance_value}"
                )

        weighted_score = compliance_value * risk_weight
        S += weighted_score

    if W == 0:
        raise ValueError("INVALID_BASELINE: Total risk weight (W) is zero.")

    framework_score = S / W

    if not 0.0 <= framework_score <= 1.0:
        raise ValueError("Computed score outside valid domain (0.00–1.00).")

    rounded_score = round(framework_score, 2)
    percent_score = round(rounded_score * 100, 2)

    risk_level = classify(percent_score)

    print("---- DriftGuard-DBR Scoring Result ----")
    print(f"Weighted Score Sum (S): {round(S, 4)}")
    print(f"Total Risk Weight (W): {round(W, 4)}")
    print(f"Composite Score: {rounded_score}")
    print(f"Composite Score (%): {percent_score}%")
    print(f"Risk Classification: {risk_level}")
    print("----------------------------------------")


if __name__ == "__main__":
    main()
