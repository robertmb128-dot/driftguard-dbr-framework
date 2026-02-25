# DriftGuard-DBR Framework – Risk Classification Model

## Purpose

This document defines how **risk and compliance scores** are calculated for DriftGuard-DBR controls.  
Scores provide a **quantitative measure of organizational database reliability and security posture**.

---

## Severity Levels

| Severity  | Weight | Description |
|-----------|--------|-------------|
| Critical  | 5      | Failure could result in major data loss, breach, or downtime |
| High      | 3      | Significant operational or security impact |
| Medium    | 2      | Moderate impact, may require attention soon |
| Low       | 1      | Minor impact, mostly advisory |

---

## Compliance Scoring

- Each control can be **compliant, partially compliant, or non-compliant**
- Scores are calculated as:

