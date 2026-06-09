from backend.app.governance.audit_trail import append_audit_event, get_audit_trail


def test_append_and_read_audit_event(tmp_path, monkeypatch):
    from backend.app.governance import audit_trail

    monkeypatch.setattr(audit_trail, "AUDIT_DIR", tmp_path)

    event = append_audit_event(
        run_id="test-run",
        action="EVIDENCE_GENERATED",
        actor="agent",
        details={"question": "Test question"},
    )

    events = get_audit_trail("test-run")

    assert event["action"] == "EVIDENCE_GENERATED"
    assert len(events) == 1
    assert events[0]["actor"] == "agent"
    assert events[0]["details"]["question"] == "Test question"
