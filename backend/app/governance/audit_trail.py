import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AUDIT_DIR = Path("evidence/audit")


def _audit_path(run_id: str) -> Path:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    return AUDIT_DIR / f"{run_id}.jsonl"


def append_audit_event(
    run_id: str,
    action: str,
    actor: str = "system",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "actor": actor,
        "action": action,
        "details": details or {},
    }

    path = _audit_path(run_id)

    with path.open("a", encoding="utf-8") as audit_file:
        audit_file.write(json.dumps(event) + "\n")

    return event


def get_audit_trail(run_id: str) -> list[dict[str, Any]]:
    path = _audit_path(run_id)

    if not path.exists():
        return []

    events: list[dict[str, Any]] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))

    return events
