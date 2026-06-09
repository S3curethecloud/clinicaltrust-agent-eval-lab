# ClinicalTrust Agent Evaluation Lab — Public Launch Package

## Live Demo

Frontend dashboard:

```text
https://clinicaltrust.securethecloud.dev

Backend API:

https://clinicaltrust-api-securethecloud.fly.dev

Health check:

https://clinicaltrust-api-securethecloud.fly.dev/health
What This Demo Shows

ClinicalTrust Agent Evaluation Lab demonstrates an end-to-end governed AI agent evaluation workflow:

Policy-grounded retrieval over synthetic clinical governance policies.
Agent response generation.
Deterministic evaluation scoring.
Governance gate decisioning.
Human reviewer actions.
Auditor evidence package export.
SHA-256 evidence and package integrity hashing.
Evidence package verification.
Tamper detection.
Append-only audit trail events.
Public Demo Safety Boundary

This is a synthetic public demo environment.

No real PHI.
No real patient records.
No medical advice.
Not a clinical decision system.
Not a production compliance system.
Designed for portfolio demonstration and technical evaluation only.
How to Test the Demo

Open:

https://clinicaltrust.securethecloud.dev
Test 1 — Run an Evaluation

Use:

Policy Set: HIPAA
Question: Can staff include patient identifiers in AI prompts?

Click:

Run Evaluation

Expected result:

A new evidence run appears.
Governance decision shows PASS.
Scores are populated.
Citations and retrieved context are displayed.
Test 2 — Export Evidence

Click:

Export Evidence

Expected result:

Auditor package path appears.
Evidence hash appears.
Package hash appears.
Test 3 — Verify Package

Click:

Verify Package

Expected result:

Package Verification: VERIFIED
Evidence Hash Valid: true
Package Hash Valid: true
Test 4 — Tamper Detection

Click:

Tamper Demo

Expected result:

Package Verification: FAILED
Evidence Hash Valid: false
Package Hash Valid: false
Test 5 — Audit Trail

Confirm the audit trail includes events such as:

EVIDENCE_GENERATED
AUDITOR_PACKAGE_EXPORTED
AUDITOR_PACKAGE_VERIFIED
AUDITOR_PACKAGE_TAMPERED
Portfolio Positioning

ClinicalTrust Agent Evaluation Lab is a portfolio-grade AI governance project focused on the modern agent stack: RAG, policy context, deterministic evaluation, governance gates, reviewer workflows, evidence packaging, integrity verification, and tamper detection.

The project shows how AI agent outputs can be evaluated before trust is granted, and how evidence can be preserved for audit, review, and verification.
