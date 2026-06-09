import copy
import hashlib
import json
from typing import Any


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_payload(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest()


def evidence_payload_for_hash(evidence: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(evidence)

    # Runtime read metadata is useful to display but should not affect evidence identity.
    payload.pop("found", None)
    payload.pop("path", None)

    return payload


def package_payload_for_hash(package: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(package)

    manifest = payload.get("export_manifest")
    if isinstance(manifest, dict):
        manifest.pop("package_hash", None)

    return payload


def build_export_manifest(package: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    evidence_hash = sha256_payload(evidence_payload_for_hash(evidence))

    manifest = {
        "manifest_type": "ClinicalTrust Evidence Integrity Manifest",
        "manifest_version": "1.0",
        "hash_algorithm": "SHA-256",
        "signature_type": "sha256_integrity_manifest",
        "evidence_hash": evidence_hash,
        "package_hash": None,
        "included_sections": [
            "governance_statement",
            "evidence",
            "governance_decision",
            "audit_trail",
        ],
        "integrity_statement": (
            "The evidence_hash is calculated from the canonical evidence payload. "
            "The package_hash is calculated from the canonical export package with "
            "the package_hash field omitted."
        ),
    }

    package["export_manifest"] = manifest
    manifest["package_hash"] = sha256_payload(package_payload_for_hash(package))

    return manifest
