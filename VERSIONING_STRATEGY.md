# DriftGuard-DBR Framework – Versioning Strategy

## Purpose

Defines the versioning methodology for controls and baselines within the DriftGuard-DBR Framework.  
Ensures **auditable integrity**, traceability of changes, and reproducible compliance scoring.

---

## Version Types

### 1. Control Version
- Each control has its own `version` attribute.
- Semantic versioning: `MAJOR.MINOR.PATCH`
  - **MAJOR**: Incompatible changes to control definition or scope  
  - **MINOR**: Additions or clarifications that do not change enforcement  
  - **PATCH**: Typo fixes, documentation, or minor adjustments  
- Example: `AC-001 version 1.0` → minor update → `1.1`  

### 2. Baseline Version
- Baselines reference **specific control versions**.
- Format: `vX.Y` (X = major baseline, Y = minor update)
- Example: `v1.0` baseline references AC-001 v1.0, ENC-001 v1.0  

### 3. Audit Traceability
- Every baseline and control version includes:
  - `date_created`
  - `last_reviewed`
  - `audit_notes`
- Enables full historical reconstruction of compliance posture.

---

## Workflow for Updating Controls

1. Identify the control requiring change.  
2. Increment version according to semantic rules.  
3. Update `last_reviewed` and `audit_notes`.  
4. Commit new control version to the repository.  
5. Update baselines referencing the control if applicable.  

---

## Workflow for Baseline Updates

1. Evaluate controls for changes, additions, or deprecations.  
2. Increment baseline minor or major version as appropriate.  
3. Reference updated control versions.  
4. Update `date_created` and `description`.  
5. Commit baseline update for audit traceability.  

---

**Outcome:** All controls and baselines are versioned, traceable, and auditable.
