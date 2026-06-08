import json
from pathlib import Path

from backend.app.schemas.evidence import EvidenceRecord


EVIDENCE_DIR = Path("evidence/runs")


def save_evidence_record(record: EvidenceRecord) -> Path:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    output_path = EVIDENCE_DIR / f"{record.run_id}.json"
    output_path.write_text(
        json.dumps(record.model_dump(), indent=2),
        encoding="utf-8",
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

    return payload
