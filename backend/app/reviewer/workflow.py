import json
from pathlib import Path

from backend.app.schemas.evidence import ReviewerStatus
from backend.app.governance.gates import evaluate_governance_decision


EVIDENCE_DIR = Path("evidence/runs")


def update_reviewer_status(run_id: str, status: ReviewerStatus) -> dict:
    evidence_path = EVIDENCE_DIR / f"{run_id}.json"

    if not evidence_path.exists():
        return {
            "updated": False,
            "run_id": run_id,
            "error": "Evidence record not found",
        }

    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    governance_decision = evaluate_governance_decision(payload)

    if status == "APPROVED" and not governance_decision["approval_allowed"]:
        return {
            "updated": False,
            "run_id": run_id,
            "requested_status": status,
            "error": "Approval blocked by governance gate",
            "governance_decision": governance_decision,
        }

    payload["reviewer_status"] = status

    evidence_path.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    return {
        "updated": True,
        "run_id": run_id,
        "reviewer_status": status,
        "path": str(evidence_path),
    }
