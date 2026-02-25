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

