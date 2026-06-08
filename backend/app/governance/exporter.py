import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.governance.evidence_store import get_evidence_record


EXPORT_DIR = Path("evidence/exports")


def export_evidence_package(run_id: str) -> dict:
    record = get_evidence_record(run_id)

    if not record.get("found"):
        return {
            "exported": False,
            "run_id": run_id,
            "error": "Evidence record not found",
        }

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    package = {
        "package_type": "ClinicalTrust Auditor Evidence Package",
        "package_version": "1.0",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "governance_statement": (
            "This package preserves the question, retrieved context, generated answer, "
            "citations, evaluation scores, reviewer status, and evidence metadata for "
            "human audit and governance review."
        ),
        "evidence": record,
    }

    output_path = EXPORT_DIR / f"{run_id}.auditor_package.json"
    output_path.write_text(
        json.dumps(package, indent=2),
        encoding="utf-8",
    )

    return {
        "exported": True,
        "run_id": run_id,
        "path": str(output_path),
        "package": package,
    }
