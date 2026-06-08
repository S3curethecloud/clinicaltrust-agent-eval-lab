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
