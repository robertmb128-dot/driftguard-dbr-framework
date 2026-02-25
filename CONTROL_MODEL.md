# DriftGuard-DBR Framework – Control Model

## Overview

The Control Model defines the authoritative representation of database reliability and security controls.  
It establishes how each control is described, classified, scored, and versioned, enabling consistent enforcement, auditing, and governance across all environments.

This model is engine-agnostic, allowing the same control definition to apply to PostgreSQL, Oracle, SQL Server, MySQL, and cloud-native databases via adapter implementations.  

It is designed to support governance, auditability, measurable reliability, and operational guidance.

## Control Object Schema

| Attribute | Type | Description |
|-----------|------|-------------|
| id | string | Unique identifier for the control (e.g., AC-001). |
| name | string | Human-readable control name. |
| category | string | Logical grouping (Access, Backup, Encryption, Monitoring). |
| description | string | Detailed explanation of the control purpose and scope. |
| engine_agnostic | boolean | Indicates if the control applies across all engines. |
| adapter_specific | list | Optional: maps to engine-specific validation logic. |
| severity | enum | Risk level: Critical, High, Medium, Low. |
| impact | string | Operational or security consequences if non-compliant. |
| baseline_reference | string | Versioned baseline this control belongs to (e.g., v1.0). |
| version | string | Control definition version. |
| compliance_score | number | Numeric value representing partial/full compliance. |
| last_reviewed | date | Date of last review for governance purposes. |
| remediation_guidance | string | Recommended steps to bring non-compliant systems into compliance. |
| audit_notes | string | Notes to capture audit justification or exceptions. |

## Categories of Controls

1. Access Controls – user roles, privileges, authentication policies  
2. Encryption Controls – at-rest and in-transit encryption, key management  
3. Backup & Recovery Controls – backup frequency, retention, recovery testing  
4. Configuration Controls – database settings, parameters, and hardening standards  
5. Monitoring Controls – logging, alerting, anomaly detection  
6. Operational Recovery Controls – failover, disaster recovery readiness, incident response  

## Compliance Scoring Model

- Each control contributes to a composite compliance score for an environment  
- Scoring is weighted by severity and operational impact  
- Scores support baseline comparisons, trend analysis, and audit reporting  

Example scoring approach:

| Severity | Weight |
|----------|--------|
| Critical | 5 |
| High     | 3 |
| Medium   | 2 |
| Low      | 1 |

Partial compliance reduces the score proportionally, enabling nuanced evaluation.

## Versioning & Change Management

- Controls are versioned independently of baselines  
- Every change must include version increment, last_reviewed timestamp, and audit_notes  
- Baselines reference specific control versions to preserve historical compliance snapshots

## Purpose & Governance

This model ensures:

- Consistency – same controls across all engines and environments  
- Authority – controls are policy-first, operational implementation second  
- Auditable Integrity – traceable metadata, version history, and review records  
- Scalable Governance – new engines, baselines, and compliance workflows can be integrated without redefining the model

