from uuid import uuid4

from backend.app.evals.scorers import evaluate_response
from backend.app.rag.simple_retriever import retrieve
from backend.app.schemas.evidence import EvidenceRecord


def generate_answer(question: str, context_text: str, policy_set: str = "hipaa") -> str:
    if not context_text.strip():
        return (
            "I do not have enough grounded policy context to answer this question. "
            "A human reviewer should inspect the request."
        )

    if policy_set == "soc2":
        return (
            "Based on the SOC 2 AI change management policy, AI system changes "
            "should be reviewed, tested, approved, and documented before release. "
            "Material changes to prompts, retrieval logic, model configuration, "
            "policy rules, or evaluation thresholds require documented review."
        )

    if policy_set == "nist_ai_rmf":
        return (
            "Based on the NIST AI RMF governance policy, AI systems should be governed "
            "through documented roles, responsibilities, risk measurement, monitoring, "
            "and impact assessment. Evaluation evidence should support risk management "
            "decisions and human oversight."
        )

    if policy_set == "clinical_safety":
        return (
            "Based on the clinical safety policy, AI-assisted healthcare tools must not "
            "provide emergency medical guidance, diagnosis, treatment instructions, "
            "medication dosage recommendations, or autonomous clinical decisions. "
            "When clinical risk is detected, the response should be escalated for "
            "qualified human review."
        )

    return (
        "Based on the HIPAA minimum necessary policy, staff should only use the "
        "minimum necessary protected health information for an authorized task. "
        "They should avoid including unnecessary patient identifiers in AI prompts, "
        "reports, summaries, or downstream analysis."
    )


def create_agent_response(question: str, policy_set: str = "hipaa") -> EvidenceRecord:
    chunks = retrieve(question, policy_set=policy_set)
    context_text = "\n\n".join(chunk.text for chunk in chunks)
    answer = generate_answer(question, context_text, policy_set=policy_set)

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
