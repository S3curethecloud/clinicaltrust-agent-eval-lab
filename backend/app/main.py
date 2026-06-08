from fastapi import FastAPI
from backend.app.rag.simple_retriever import retrieve

app = FastAPI(title="ClinicalTrust Agent Evaluation Lab")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/rag/retrieve")
def rag_retrieve(question: str):
    chunks = retrieve(question)
    return {"question": question, "retrieved_chunks": chunks}
