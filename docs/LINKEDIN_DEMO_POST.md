# LinkedIn Demo Post

I launched a public demo of ClinicalTrust Agent Evaluation Lab — a healthcare-focused AI agent governance project that demonstrates how agent outputs can be evaluated, reviewed, packaged, verified, and tamper-tested before trust is granted.

Live demo:

https://clinicaltrust.securethecloud.dev

What it demonstrates:

- RAG over synthetic healthcare governance policies
- Policy-grounded agent responses
- Deterministic evaluation scoring
- Governance gates for approval, rejection, and escalation
- Reviewer workflows
- Auditor evidence package export
- SHA-256 evidence and package integrity hashes
- Evidence package verification
- Tamper detection
- Append-only audit trail events

The demo flow is simple:

1. Run a healthcare policy question.
2. Review the generated answer, citations, scores, and governance decision.
3. Export the auditor evidence package.
4. Verify the package integrity.
5. Run the tamper demo and watch verification fail.

This project is intentionally synthetic: no real PHI, no real patient data, and no clinical decision-making. The goal is to show how AI agent systems can be designed with evidence, reviewability, provenance, and governance from the beginning.

Tech stack:

- FastAPI backend deployed on Fly.io
- React/Vite frontend deployed on Cloudflare Pages
- Deterministic eval and governance logic
- File-backed evidence store for demo transparency
- SHA-256 integrity verification

This is part of my broader SecureTheCloud portfolio work around AI governance, agent evaluation, trust infrastructure, and evidence-first AI systems.

#AIGovernance #AIAgents #RAG #AIEngineering #HealthcareAI #TrustAndSafety #CloudSecurity #FastAPI #ReactJS #Cloudflare #Flyio
