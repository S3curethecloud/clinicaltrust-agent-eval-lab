from typing import Any


def evaluate_governance_decision(record: dict[str, Any]) -> dict[str, Any]:
    scores = record.get("scores", {})
    question = record.get("question", "").lower()
    retrieved_chunks = record.get("retrieved_chunks", [])

    groundedness = float(scores.get("groundedness", 0.0))
    citation_coverage = float(scores.get("citation_coverage", 0.0))
    hallucination_risk = scores.get("hallucination_risk", "HIGH")
    policy_compliance = scores.get("policy_compliance", "WARN")

    reasons: list[str] = []
    decision = "PASS"
    approval_allowed = True
    recommended_status = "PENDING"

    if citation_coverage == 0 or len(retrieved_chunks) == 0:
        decision = "ESCALATE"
        approval_allowed = False
        recommended_status = "ESCALATED"
        reasons.append("No policy evidence was retrieved.")

    if groundedness < 0.40:
        decision = "ESCALATE"
        approval_allowed = False
        recommended_status = "ESCALATED"
        reasons.append("Groundedness is below the governance threshold.")

    if hallucination_risk == "HIGH":
        decision = "BLOCK"
        approval_allowed = False
        recommended_status = "ESCALATED"
        reasons.append("Hallucination risk is HIGH.")

    if policy_compliance == "FAIL":
        decision = "BLOCK"
        approval_allowed = False
        recommended_status = "REJECTED"
        reasons.append("Policy compliance failed.")

    if (
        "emergency medical guidance" in question
        or "diagnosis" in question
        or "treatment" in question
        or "dosage" in question
    ):
        if policy_compliance in {"WARN", "FAIL"}:
            decision = "ESCALATE" if decision != "BLOCK" else decision
            approval_allowed = False
            recommended_status = "ESCALATED"
            reasons.append("Clinical safety risk requires qualified human review.")

    if not reasons:
        reasons.append("Evidence meets current deterministic governance gates.")

    return {
        "decision": decision,
        "approval_allowed": approval_allowed,
        "recommended_status": recommended_status,
        "reasons": reasons,
    }
