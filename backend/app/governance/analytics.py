from backend.app.governance.evidence_store import list_evidence_records, get_evidence_record


def _avg(values: list[float]) -> float:
    if not values:
        return 0.0

    return round(sum(values) / len(values), 2)


def get_governance_analytics() -> dict:
    summaries = list_evidence_records()
    details = [
        get_evidence_record(record["run_id"])
        for record in summaries
        if record.get("run_id")
    ]

    total = len(details)
    approved = sum(1 for item in details if item.get("reviewer_status") == "APPROVED")
    rejected = sum(1 for item in details if item.get("reviewer_status") == "REJECTED")
    escalated = sum(1 for item in details if item.get("reviewer_status") == "ESCALATED")
    pending = sum(1 for item in details if item.get("reviewer_status") == "PENDING")

    high_risk = sum(
        1
        for item in details
        if item.get("scores", {}).get("hallucination_risk") == "HIGH"
    )

    medium_risk = sum(
        1
        for item in details
        if item.get("scores", {}).get("hallucination_risk") == "MEDIUM"
    )

    low_risk = sum(
        1
        for item in details
        if item.get("scores", {}).get("hallucination_risk") == "LOW"
    )

    policy_pass = sum(
        1
        for item in details
        if item.get("scores", {}).get("policy_compliance") == "PASS"
    )

    policy_warn = sum(
        1
        for item in details
        if item.get("scores", {}).get("policy_compliance") == "WARN"
    )

    policy_fail = sum(
        1
        for item in details
        if item.get("scores", {}).get("policy_compliance") == "FAIL"
    )

    groundedness = [
        float(item.get("scores", {}).get("groundedness", 0.0))
        for item in details
    ]

    relevance = [
        float(item.get("scores", {}).get("relevance", 0.0))
        for item in details
    ]

    citation_coverage = [
        float(item.get("scores", {}).get("citation_coverage", 0.0))
        for item in details
    ]

    approval_rate = round(approved / total, 2) if total else 0.0
    escalation_rate = round(escalated / total, 2) if total else 0.0
    rejection_rate = round(rejected / total, 2) if total else 0.0

    return {
        "total_runs": total,
        "review_status": {
            "approved": approved,
            "rejected": rejected,
            "escalated": escalated,
            "pending": pending,
        },
        "risk_distribution": {
            "low": low_risk,
            "medium": medium_risk,
            "high": high_risk,
        },
        "policy_distribution": {
            "pass": policy_pass,
            "warn": policy_warn,
            "fail": policy_fail,
        },
        "rates": {
            "approval_rate": approval_rate,
            "escalation_rate": escalation_rate,
            "rejection_rate": rejection_rate,
        },
        "averages": {
            "groundedness": _avg(groundedness),
            "relevance": _avg(relevance),
            "citation_coverage": _avg(citation_coverage),
        },
    }
