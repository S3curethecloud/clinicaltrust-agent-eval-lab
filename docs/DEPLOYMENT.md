# ClinicalTrust Agent Evaluation Lab — Public Demo Deployment

## Target Architecture

- Frontend dashboard: Cloudflare Pages
- Backend API: Fly.io
- Runtime mode: public demo using synthetic evidence only

## Public Demo Safety Statement

This project is a synthetic clinical AI governance demo. It does not process real PHI, does not provide medical advice, and is not a production clinical decision system.

## Backend API Deployment — Fly.io

The backend is a FastAPI service packaged with Docker.

### Files

- `Dockerfile`
- `fly.toml`
- `requirements.txt`
- `backend/`
- `data/`

### Deploy

From the repository root:

```bash
fly auth login
fly launch --no-deploy
fly deploy

If the app name in fly.toml is unavailable, change:

app = "clinicaltrust-agent-eval-lab-api"

Then deploy again.

Verify
curl "https://clinicaltrust-agent-eval-lab-api.fly.dev/health"

Expected:

{"status":"ok"}
Frontend Deployment — Cloudflare Pages

The frontend is a Vite React application.

Cloudflare Pages Settings
Root directory: frontend
Build command: npm run build
Build output directory: dist
Environment Variable

Set this in Cloudflare Pages:

VITE_API_BASE_URL=https://clinicaltrust-agent-eval-lab-api.fly.dev
CORS

The backend reads allowed origins from:

ALLOWED_ORIGINS

Example Fly value:

http://localhost:5173,http://127.0.0.1:5173,https://clinicaltrust-agent-eval-lab.pages.dev

If using a custom Cloudflare Pages domain, append that domain to ALLOWED_ORIGINS.

Public Demo Flow
Open the Cloudflare Pages dashboard URL.
Run a policy-grounded evaluation.
Review scores and governance gate result.
Export auditor evidence package.
Verify package integrity.
Run tamper demo.
Verify again and observe hash failure.
Demo Limitations
Evidence is synthetic.
Runtime evidence files are demo artifacts.
No real PHI should be entered.
No production clinical decisions should be made from this app.
