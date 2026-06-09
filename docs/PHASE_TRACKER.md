
ClinicalTrust Phase Tracker
Current Phase

Status: Phase 1 Foundation In Progress

Phase 1 - Foundation
 Repository cloned
 Base folder structure created
 README created
 Architecture document created
 Governance document created
 Roadmap created
 Initial commit pushed
Phase 2 - RAG Layer
 Sample healthcare policy corpus
 Document chunking
 Retrieval abstraction
 Citation metadata
Phase 3 - Agent Response Layer
 Agent response schema
 Retriever/generator workflow
 Mock model adapter
 Azure OpenAI adapter placeholder
Phase 4 - Evaluation Layer
 Groundedness scoring
 Relevance scoring
 Citation coverage scoring
 Hallucination risk scoring
 Policy compliance scoring
Phase 5 - Governance Evidence Layer
 Evidence package schema
 Evidence JSON output
 Reviewer status
 Audit trail
Phase 6 - Dashboard
 React app shell
 Evaluation run history
 Evidence explorer
 Reviewer workflow

## Phase 16 — Public Demo Deployment Prep

Status: Complete

- [x] Dockerfile added for FastAPI backend.
- [x] Fly.io `fly.toml` deployment config added.
- [x] Frontend API base URL moved to `VITE_API_BASE_URL`.
- [x] Production CORS allowlist added.
- [x] Public demo disclaimer banner added.
- [x] Mobile polish added for dashboard layout, action buttons, and hash wrapping.
- [x] Public deployment instructions added.
- [x] README public demo section added.

Deployment target:

- Backend API: Fly.io
- Frontend dashboard: Cloudflare Pages

Safety boundary:

- Synthetic evidence only.
- No real PHI.
- Not a production clinical decision system.

Phase 19 — Public Launch Polish / LinkedIn Demo Package

Status: Complete

 Live public frontend custom domain recorded.
 Live public backend API URL recorded.
 README public demo testing steps added.
 Public launch package added.
 LinkedIn-ready demo post added.
 Custom domain activated.

Public frontend:

https://clinicaltrust.securethecloud.dev

Public backend:

https://clinicaltrust-api-securethecloud.fly.dev

Demo validation:

Run evaluation.
Export auditor package.
Verify evidence package.
Apply tamper demo.
Confirm verification failure.
Confirm audit trail events.

Safety boundary:

Synthetic evidence only.
No real PHI.
No medical advice.
Not a production clinical decision system.
