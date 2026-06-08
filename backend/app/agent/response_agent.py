from uuid import uuid4

from backend.app.rag.simple_retriever import retrieve
from backend.app.schemas.evidence import EvidenceRecord
from backend.app.evals.scorers import evaluate_response


def generate_answer(question: str, context_text: str) -> str:
    if not context_text.strip():
        return (
            "I do not have enough grounded policy context to answer this question. "
            "A human reviewer should inspect the request."
        )

    return (
        "Based on the available healthcare policy context, staff should only use the "
        "minimum necessary protected health information for an authorized task. "
        "They should avoid including unnecessary patient identifiers in AI prompts, "
        "reports, summaries, or downstream analysis."
    )


def create_agent_response(question: str) -> EvidenceRecord:
    chunks = retrieve(question)
    context_text = "\n\n".join(chunk.text for chunk in chunks)
    answer = generate_answer(question, context_text)

    citations = [chunk.source for chunk in chunks]

    scores = evaluate_response(
        question=question,
        answer=answer,
        chunks=chunks,
        citations=citations,
    )

    return EvidenceRecord(
        run_id=str(uuid4()),
        question=question,
        retrieved_chunks=chunks,
        answer=answer,
        citations=citations,
        scores=scores,
        reviewer_status="PENDING",
    )
