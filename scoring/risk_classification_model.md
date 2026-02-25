# DriftGuard-DBR Framework – Risk Classification Model

## Compliance Factor
- Fully compliant = 1.0  
- Partially compliant = 0.5  
- Non-compliant = 0  

**Example:** AC-002 (Critical, Weight=5)  
- Fully compliant → 5 × 1.0 = 5  
- Partially compliant → 5 × 0.5 = 2.5  
- Non-compliant → 5 × 0 = 0  

---

## Composite Environment Score
- Expressed as **percentage compliance**  
- Supports **trend tracking, audit reporting, and baseline comparison**

---

## Risk Classification

| Composite Score | Risk Level        |
|-----------------|-----------------|
| 90–100%         | Excellent       |
| 75–89%          | Good            |
| 50–74%          | Moderate        |
| 25–49%          | High Risk       |
| 0–24%           | Critical Risk   |

- Risk levels guide **remediation prioritization** and operational focus.

---

## Notes
- Scores are **engine-agnostic**; adapters calculate compliance per engine.  
- Future baselines may **update control weights** to reflect evolving risk posture.  
- This model ensures **consistent, auditable, and repeatable compliance scoring**.
