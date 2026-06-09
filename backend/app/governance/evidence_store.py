import json
from pathlib import Path

from backend.app.governance.gates import evaluate_governance_decision
from backend.app.governance.audit_trail import append_audit_event, get_audit_trail

from backend.app.schemas.evidence import EvidenceRecord


EVIDENCE_DIR = Path("evidence/runs")


def save_evidence_record(record: EvidenceRecord) -> Path:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    output_path = EVIDENCE_DIR / f"{record.run_id}.json"
    output_path.write_text(
        json.dumps(record.model_dump(), indent=2),
        encoding="utf-8",
    )

    append_audit_event(
        run_id=record.run_id,
        action="EVIDENCE_GENERATED",
        actor="agent",
        details={
            "question": record.question,
            "reviewer_status": record.reviewer_status,
            "hallucination_risk": record.scores.hallucination_risk,
            "policy_compliance": record.scores.policy_compliance,
        },
    )

    return output_path


def list_evidence_records() -> list[dict]:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []

    for path in sorted(EVIDENCE_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(
            {
                "run_id": payload.get("run_id"),
                "question": payload.get("question"),
                "reviewer_status": payload.get("reviewer_status"),
                "hallucination_risk": payload.get("scores", {}).get("hallucination_risk"),
                "policy_compliance": payload.get("scores", {}).get("policy_compliance"),
                "path": str(path),
            }
        )

    return records


def get_evidence_record(run_id: str) -> dict:
    evidence_path = EVIDENCE_DIR / f"{run_id}.json"

    if not evidence_path.exists():
        return {
            "found": False,
            "run_id": run_id,
            "error": "Evidence record not found",
        }

    payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    payload["found"] = True
    payload["path"] = str(evidence_path)
    payload["governance_decision"] = evaluate_governance_decision(payload)
    payload["audit_trail"] = get_audit_trail(run_id)

    return payload
