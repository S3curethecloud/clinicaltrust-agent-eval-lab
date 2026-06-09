import json

from backend.app.governance.integrity import build_export_manifest
from backend.app.governance.tamper_demo import tamper_evidence_package
from backend.app.governance.verifier import verify_evidence_package


def test_tamper_demo_causes_package_verification_failure(tmp_path, monkeypatch):
    from backend.app.governance import audit_trail, tamper_demo, verifier

    monkeypatch.setattr(tamper_demo, "EXPORT_DIR", tmp_path)
    monkeypatch.setattr(verifier, "EXPORT_DIR", tmp_path)
    monkeypatch.setattr(audit_trail, "AUDIT_DIR", tmp_path / "audit")

    evidence = {
        "run_id": "run-tamper",
        "question": "Can staff include patient identifiers?",
        "answer": "Original answer",
        "scores": {"groundedness": 0.9},
    }

    package = {
        "package_type": "ClinicalTrust Auditor Evidence Package",
        "package_version": "1.0",
        "evidence": evidence,
    }

    build_export_manifest(package, evidence)

    output_path = tmp_path / "run-tamper.auditor_package.json"
    output_path.write_text(json.dumps(package, indent=2), encoding="utf-8")

    tamper_result = tamper_evidence_package("run-tamper")
    verify_result = verify_evidence_package("run-tamper")

    assert tamper_result["tampered"] is True
    assert verify_result["verified"] is False
    assert verify_result["evidence_hash_valid"] is False
    assert verify_result["package_hash_valid"] is False
