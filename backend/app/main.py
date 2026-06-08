from fastapi import FastAPI
from backend.app.rag.simple_retriever import retrieve
from backend.app.agent.response_agent import create_agent_response

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
    return create_agent_response(question)
