from backend.app.governance.integrity import (
    build_export_manifest,
    evidence_payload_for_hash,
    package_payload_for_hash,
    sha256_payload,
)


def test_sha256_payload_is_stable_for_key_order():
    left = {"b": 2, "a": 1}
    right = {"a": 1, "b": 2}

    assert sha256_payload(left) == sha256_payload(right)


def test_evidence_hash_excludes_runtime_read_metadata():
    evidence = {
        "run_id": "run-1",
        "question": "Test?",
        "found": True,
        "path": "evidence/runs/run-1.json",
    }

    normalized = evidence_payload_for_hash(evidence)

    assert "found" not in normalized
    assert "path" not in normalized


def test_build_export_manifest_adds_evidence_and_package_hashes():
    evidence = {
        "run_id": "run-1",
        "question": "Test?",
        "scores": {"groundedness": 1.0},
    }

    package = {
        "package_type": "ClinicalTrust Auditor Evidence Package",
        "package_version": "1.0",
        "evidence": evidence,
    }

    manifest = build_export_manifest(package, evidence)

    assert manifest["hash_algorithm"] == "SHA-256"
    assert len(manifest["evidence_hash"]) == 64
    assert len(manifest["package_hash"]) == 64
    assert package["export_manifest"]["package_hash"] == manifest["package_hash"]

    # Recompute the package hash using the same omitted-package-hash rule.
    assert sha256_payload(package_payload_for_hash(package)) == manifest["package_hash"]
