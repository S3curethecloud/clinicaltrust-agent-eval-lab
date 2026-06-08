from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.rag.simple_retriever import retrieve
from backend.app.agent.response_agent import create_agent_response
from backend.app.governance.evidence_store import get_evidence_record, list_evidence_records, save_evidence_record
from backend.app.governance.analytics import get_governance_analytics
from backend.app.reviewer.workflow import update_reviewer_status
from backend.app.benchmark.runner import run_benchmark

app = FastAPI(title="ClinicalTrust Agent Evaluation Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rag/retrieve")
def rag_retrieve(question: str):
    chunks = retrieve(question)
    return {"question": question, "retrieved_chunks": chunks}


@app.get("/agent/respond")
def agent_respond(question: str):
    record = create_agent_response(question)
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
def benchmark_run():
    results = run_benchmark()

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
