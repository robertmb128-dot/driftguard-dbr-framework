# DriftGuard-DBR Framework – Evaluation Model

## 1. Purpose

Defines the deterministic algorithm used to calculate control compliance and composite environment scores.

This model ensures scoring is:
- Consistent
- Auditable
- Engine-agnostic
- Mathematically reproducible

---

## 2. Control-Level Compliance Values

Each control must resolve to one of the following values:

| State               | Value |
|--------------------|-------|
| Fully Compliant     | 1.0   |
| Partially Compliant | 0.5   |
| Non-Compliant       | 0.0   |

Adapters are responsible for determining compliance state.

---

## 3. Severity Weights

Each control contributes weight based on severity:

| Severity  | Weight |
|-----------|--------|
| Critical  | 5      |
| High      | 3      |
| Medium    | 2      |
| Low       | 1      |

---

## 4. Weighted Control Score

For each control:


Example:

Critical control (weight=5)
- Fully compliant → 5 × 1.0 = 5
- Partially compliant → 5 × 0.5 = 2.5
- Non-compliant → 5 × 0 = 0

---

## 5. Composite Environment Score

Let:

- W = Sum of all severity weights in baseline
- S = Sum of all weighted control scores

Then:

---

## 6. Rounding Standard

- Scores are rounded to 2 decimal places.
- Risk classification uses rounded value.

---

## 7. Missing Control Handling

If a control cannot be evaluated:
- It is treated as Non-Compliant (0.0)
- Unless an approved exception exists

---

## 8. Exception Handling

If a control has an approved exception:
- It contributes full weight (1.0)
- Must include documented justification
- Must include expiration date

---

## 9. Risk Classification

| Composite Score | Risk Level     |
|-----------------|---------------|
| 90–100%         | Excellent     |
| 75–89%          | Good          |
| 50–74%          | Moderate      |
| 25–49%          | High Risk     |
| 0–24%           | Critical Risk |

---

## 10. Deterministic Guarantee

Given:
- A baseline version
- Control versions
- Compliance results

The composite score must always produce the same output.
