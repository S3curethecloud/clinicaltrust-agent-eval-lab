import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.rag.simple_retriever import list_policy_sets, retrieve
from backend.app.agent.response_agent import create_agent_response
from backend.app.governance.evidence_store import get_evidence_record, list_evidence_records, save_evidence_record
from backend.app.governance.analytics import get_governance_analytics
from backend.app.governance.audit_trail import get_audit_trail
from backend.app.governance.exporter import export_evidence_package
from backend.app.governance.verifier import verify_evidence_package
from backend.app.governance.tamper_demo import tamper_evidence_package
from backend.app.reviewer.workflow import update_reviewer_status
from backend.app.benchmark.runner import run_benchmark

DEFAULT_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://clinicaltrust-agent-eval-lab.pages.dev",
]


def get_allowed_origins() -> list[str]:
    configured = os.getenv("ALLOWED_ORIGINS", "")
    configured_origins = [
        origin.strip()
        for origin in configured.split(",")
        if origin.strip()
    ]

    return sorted(set(DEFAULT_ALLOWED_ORIGINS + configured_origins))


app = FastAPI(title="ClinicalTrust Agent Evaluation Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rag/retrieve")
def rag_retrieve(question: str, policy_set: str = "hipaa"):
    chunks = retrieve(question, policy_set=policy_set)
    return {
        "question": question,
        "policy_set": policy_set,
        "retrieved_chunks": chunks,
    }


@app.get("/agent/respond")
def agent_respond(question: str, policy_set: str = "hipaa"):
    record = create_agent_response(question, policy_set=policy_set)
    save_evidence_record(record)
    return record


@app.get("/governance/evidence")
def governance_evidence():
    return {"records": list_evidence_records()}


@app.post("/reviewer/status")
def reviewer_status(run_id: str, status: str):
    return update_reviewer_status(run_id, status)


@app.get("/governance/evidence/{run_id}")
def governance_evidence_detail(run_id: str):
    return get_evidence_record(run_id)


@app.get("/governance/analytics")
def governance_analytics():
    return get_governance_analytics()

@app.post("/benchmark/run")
def benchmark_run(policy_set: str = "hipaa"):
    results = run_benchmark(policy_set=policy_set)

    total = len(results)

    avg_groundedness = round(
        sum(r["groundedness"] for r in results) / total,
        2,
    )

    avg_relevance = round(
        sum(r["relevance"] for r in results) / total,
        2,
    )

    return {
        "total_questions": total,
        "average_groundedness": avg_groundedness,
        "average_relevance": avg_relevance,
        "results": results,
    }


@app.get("/policy-sets")
def policy_sets():
    return {"policy_sets": list_policy_sets()}


@app.post("/governance/evidence/{run_id}/export")
def governance_evidence_export(run_id: str):
    return export_evidence_package(run_id)


@app.get("/governance/evidence/{run_id}/audit")
def governance_evidence_audit(run_id: str):
    return {"run_id": run_id, "audit_trail": get_audit_trail(run_id)}


@app.post("/governance/evidence/{run_id}/verify")
def governance_evidence_verify(run_id: str):
    return verify_evidence_package(run_id)


@app.post("/governance/evidence/{run_id}/tamper-demo")
def governance_evidence_tamper_demo(run_id: str):
    return tamper_evidence_package(run_id)
