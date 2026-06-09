import json

from backend.app.governance.integrity import build_export_manifest
from backend.app.governance.verifier import verify_evidence_package


def test_verify_evidence_package_passes_for_untampered_package(tmp_path, monkeypatch):
    from backend.app.governance import verifier

    monkeypatch.setattr(verifier, "EXPORT_DIR", tmp_path)

    evidence = {
        "run_id": "run-1",
        "question": "Can staff include patient identifiers?",
        "scores": {"groundedness": 0.9},
    }

    package = {
        "package_type": "ClinicalTrust Auditor Evidence Package",
        "package_version": "1.0",
        "evidence": evidence,
    }

    build_export_manifest(package, evidence)

    output_path = tmp_path / "run-1.auditor_package.json"
    output_path.write_text(json.dumps(package, indent=2), encoding="utf-8")

    result = verify_evidence_package("run-1")

    assert result["verified"] is True
    assert result["evidence_hash_valid"] is True
    assert result["package_hash_valid"] is True


def test_verify_evidence_package_fails_when_evidence_is_tampered(tmp_path, monkeypatch):
    from backend.app.governance import verifier

    monkeypatch.setattr(verifier, "EXPORT_DIR", tmp_path)

    evidence = {
        "run_id": "run-2",
        "question": "Original question",
        "scores": {"groundedness": 0.9},
    }

    package = {
        "package_type": "ClinicalTrust Auditor Evidence Package",
        "package_version": "1.0",
        "evidence": evidence,
    }

    build_export_manifest(package, evidence)

    package["evidence"]["question"] = "Tampered question"

    output_path = tmp_path / "run-2.auditor_package.json"
    output_path.write_text(json.dumps(package, indent=2), encoding="utf-8")

    result = verify_evidence_package("run-2")

    assert result["verified"] is False
    assert result["evidence_hash_valid"] is False
    assert result["package_hash_valid"] is False
