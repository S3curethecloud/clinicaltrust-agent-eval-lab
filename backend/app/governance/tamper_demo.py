import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.app.governance.audit_trail import append_audit_event
from backend.app.governance.exporter import EXPORT_DIR


def _package_path(run_id: str) -> Path:
    return EXPORT_DIR / f"{run_id}.auditor_package.json"


def tamper_evidence_package(run_id: str) -> dict[str, Any]:
    package_path = _package_path(run_id)

    if not package_path.exists():
        return {
            "tampered": False,
            "run_id": run_id,
            "error": "Auditor package not found. Export the evidence package first.",
        }

    package = json.loads(package_path.read_text(encoding="utf-8"))

    evidence = package.setdefault("evidence", {})
    original_answer = evidence.get("answer", "")

    evidence["answer"] = (
        f"{original_answer}\n\n[TAMPER DEMO] This exported evidence package was intentionally modified after export."
    ).strip()

    package["tamper_demo"] = {
        "tampered": True,
        "tampered_at": datetime.now(timezone.utc).isoformat(),
        "tamper_type": "post_export_evidence_answer_mutation",
        "expected_verification_result": "FAILED",
    }

    package_path.write_text(
        json.dumps(package, indent=2),
        encoding="utf-8",
    )

    append_audit_event(
        run_id=run_id,
        action="AUDITOR_PACKAGE_TAMPERED",
        actor="demo_operator",
        details={
            "path": str(package_path),
            "tamper_type": "post_export_evidence_answer_mutation",
            "expected_verification_result": "FAILED",
        },
    )

    return {
        "tampered": True,
        "run_id": run_id,
        "path": str(package_path),
        "message": "Auditor package intentionally tampered for integrity verification demo.",
    }
