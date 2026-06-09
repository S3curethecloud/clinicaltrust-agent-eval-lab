import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.governance.evidence_store import get_evidence_record
from backend.app.governance.integrity import build_export_manifest
from backend.app.governance.audit_trail import append_audit_event


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

    export_manifest = build_export_manifest(package, record)

    output_path = EXPORT_DIR / f"{run_id}.auditor_package.json"
    output_path.write_text(
        json.dumps(package, indent=2),
        encoding="utf-8",
    )

    append_audit_event(
        run_id=run_id,
        action="AUDITOR_PACKAGE_EXPORTED",
        actor="auditor",
        details={
            "export_path": str(output_path),
            "package_version": package["package_version"],
            "evidence_hash": export_manifest["evidence_hash"],
            "package_hash": export_manifest["package_hash"],
            "hash_algorithm": export_manifest["hash_algorithm"],
        },
    )

    return {
        "exported": True,
        "run_id": run_id,
        "path": str(output_path),
        "package": package,
    }
