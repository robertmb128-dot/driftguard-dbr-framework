## DriftGuard-DBR Framework – Evaluation Model
## 1. Purpose

Defines the deterministic algorithm used to calculate control compliance and composite environment scores.

This model ensures scoring is:

Consistent

Auditable

Engine-agnostic

Mathematically reproducible

## 2. Control-Level Compliance Values

Each control must resolve to one of the following values:

State	Value
Fully Compliant	1.0
Partially Compliant	0.5
Non-Compliant	0.0

Adapters are responsible for determining the compliance state.

ComplianceValue ∈ {0.0, 0.5, 1.0}

## 3. Risk Weight Model

Each control defines an explicit risk_weight.

Default guidance:

Severity	Suggested Default
Low	0.5
Medium	1.0
High	2.0
Critical	3.0

Severity is descriptive.
risk_weight is authoritative for scoring.

## 4. Weighted Control Score

For each control:

Weighted Score = ComplianceValue × RiskWeight

Where:

ComplianceValue ∈ {0.0, 0.5, 1.0}

Example:

Critical control (weight = 3.0)

Fully compliant → 3.0 × 1.0 = 3.0

Partially compliant → 3.0 × 0.5 = 1.5

Non-compliant → 3.0 × 0.0 = 0

## 5. Composite Environment Score

Let:

W = Sum of all risk weights in the baseline
S = Sum of all weighted control scores

Then:

Framework Score = S / W

Zero-Weight Guard Condition

If:

W = 0

Then:

The scoring operation must fail and return error: INVALID_BASELINE

No score shall be produced.

## 6. Rounding Standard

Scores are rounded to 2 decimal places.

Risk classification uses the rounded value.

## 7. Missing Control Handling

If a control cannot be evaluated:

It is treated as Non-Compliant (0.0)

Unless an approved exception exists

## 8. Exception Handling

If:

status = Active

expiration_date ≥ today

Then:

ComplianceValue = 1.0

If:

expiration_date < today

Then:

ComplianceValue = 0.0

Exceptions must include:

Documented justification

Explicit expiration date

## 9. Risk Classification

Composite Score	Risk Level
90–100%	Excellent
75–89%	Good
50–74%	Moderate
25–49%	High Risk
0–24%	Critical Risk

## 10. Deterministic Guarantee

Given:

A specific baseline version

Defined control versions

Compliance results

Approved exceptions

The composite score must always produce the same output.

No discretionary logic is permitted within the scoring engine.
