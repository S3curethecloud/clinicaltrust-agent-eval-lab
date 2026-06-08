from fastapi import FastAPI
from backend.app.rag.simple_retriever import retrieve
from backend.app.agent.response_agent import create_agent_response
from backend.app.governance.evidence_store import list_evidence_records, save_evidence_record
from backend.app.reviewer.workflow import update_reviewer_status

app = FastAPI(title="ClinicalTrust Agent Evaluation Lab")


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
