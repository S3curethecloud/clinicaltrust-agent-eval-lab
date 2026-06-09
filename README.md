# ClinicalTrust Agent Evaluation Lab

Evidence-driven AI governance for healthcare RAG and agent systems.

This lab demonstrates how a healthcare AI system can move from Retrieval-Augmented Generation to evaluation, evidence generation, and human governance review.

## Core Mission

ClinicalTrust answers one question:

> Can this AI response be trusted?

## Implemented Governance Module

This project implements one focused module:

**Agent Evaluation Platform**

It evaluates RAG and agent responses for:

- Groundedness
- Relevance
- Citation quality
- Hallucination risk
- Healthcare policy compliance
- Reviewer approval status

## What This Is Not

This is not a production clinical decision system.

It does not provide medical advice, diagnose patients, or replace licensed professionals.

## Architecture

```text
Healthcare Documents
        |
        v
RAG Pipeline
        |
        v
Agent Response
        |
        v
Evaluation Engine
        |
        v
Governance Evidence Package
        |
        v
Reviewer Dashboard
Build Phases

See docs/PHASE_TRACKER.md.

## Public Demo Deployment

ClinicalTrust Agent Evaluation Lab is designed for a public portfolio demo using a split deployment model:

- Backend API on Fly.io
- Frontend dashboard on Cloudflare Pages

The public demo uses synthetic healthcare governance scenarios only. It does not process real PHI, does not provide medical advice, and is not a production clinical decision system.

The demo flow shows a full AI governance evidence lifecycle: policy-grounded retrieval, agent response generation, deterministic evaluation, governance gates, reviewer workflow, auditor evidence package export, SHA-256 package verification, and tamper detection.

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for deployment instructions.

## Live Public Demo

Frontend dashboard:

```text
https://clinicaltrust.securethecloud.dev

Backend API:

https://clinicaltrust-api-securethecloud.fly.dev

Health check:

https://clinicaltrust-api-securethecloud.fly.dev/health
How to Test the Public Demo
Open the frontend dashboard.
Run the default HIPAA evaluation question.
Select the generated evidence run.
Export the auditor evidence package.
Verify the package integrity.
Run the tamper demo.
Confirm verification fails after tampering.

Expected verification result before tampering:

Package Verification: VERIFIED
Evidence Hash Valid: true
Package Hash Valid: true

Expected verification result after tampering:

Package Verification: FAILED
Evidence Hash Valid: false
Package Hash Valid: false

Public demo boundary:

Synthetic governance evidence only.
No real PHI.
No medical advice.
Not a production clinical decision system.
