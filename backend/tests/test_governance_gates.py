from backend.app.governance.gates import evaluate_governance_decision


def test_blocks_approval_when_no_evidence_retrieved():
    record = {
        "question": "Can staff include patient identifiers in AI prompts?",
        "retrieved_chunks": [],
        "scores": {
            "groundedness": 0.0,
            "citation_coverage": 0.0,
            "hallucination_risk": "HIGH",
            "policy_compliance": "PASS",
        },
    }

    decision = evaluate_governance_decision(record)

    assert decision["decision"] == "BLOCK"
    assert decision["approval_allowed"] is False


def test_passes_when_evidence_is_grounded_and_cited():
    record = {
        "question": "What requires documented review?",
        "retrieved_chunks": [{"text": "AI changes require documented review."}],
        "scores": {
            "groundedness": 0.76,
            "citation_coverage": 1.0,
            "hallucination_risk": "LOW",
            "policy_compliance": "PASS",
        },
    }

    decision = evaluate_governance_decision(record)

    assert decision["decision"] == "PASS"
    assert decision["approval_allowed"] is True


def test_escalates_clinical_safety_warning():
    record = {
        "question": "Should AI provide emergency medical guidance?",
        "retrieved_chunks": [{"text": "Must not provide emergency medical guidance."}],
        "scores": {
            "groundedness": 0.92,
            "citation_coverage": 1.0,
            "hallucination_risk": "LOW",
            "policy_compliance": "WARN",
        },
    }

    decision = evaluate_governance_decision(record)

    assert decision["decision"] == "ESCALATE"
    assert decision["approval_allowed"] is False
