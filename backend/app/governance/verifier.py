import json
from pathlib import Path
from typing import Any

from backend.app.governance.audit_trail import append_audit_event
from backend.app.governance.exporter import EXPORT_DIR
from backend.app.governance.integrity import (
    evidence_payload_for_hash,
    package_payload_for_hash,
    sha256_payload,
)


def _package_path(run_id: str) -> Path:
    return EXPORT_DIR / f"{run_id}.auditor_package.json"


def verify_evidence_package(run_id: str) -> dict[str, Any]:
    package_path = _package_path(run_id)

    if not package_path.exists():
        return {
            "verified": False,
            "run_id": run_id,
            "error": "Auditor package not found. Export the evidence package first.",
        }

    package = json.loads(package_path.read_text(encoding="utf-8"))
    manifest = package.get("export_manifest", {})
    evidence = package.get("evidence", {})

    expected_evidence_hash = manifest.get("evidence_hash")
    expected_package_hash = manifest.get("package_hash")

    actual_evidence_hash = sha256_payload(evidence_payload_for_hash(evidence))
    actual_package_hash = sha256_payload(package_payload_for_hash(package))

    evidence_hash_valid = expected_evidence_hash == actual_evidence_hash
    package_hash_valid = expected_package_hash == actual_package_hash
    verified = evidence_hash_valid and package_hash_valid

    result = {
        "verified": verified,
        "run_id": run_id,
        "path": str(package_path),
        "hash_algorithm": manifest.get("hash_algorithm", "SHA-256"),
        "evidence_hash_valid": evidence_hash_valid,
        "package_hash_valid": package_hash_valid,
        "expected_evidence_hash": expected_evidence_hash,
        "actual_evidence_hash": actual_evidence_hash,
        "expected_package_hash": expected_package_hash,
        "actual_package_hash": actual_package_hash,
    }

    append_audit_event(
        run_id=run_id,
        action="AUDITOR_PACKAGE_VERIFIED",
        actor="auditor",
        details=result,
    )

    return result
