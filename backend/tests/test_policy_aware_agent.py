from backend.app.agent.response_agent import generate_answer


def test_soc2_answer_mentions_change_management_review():
    answer = generate_answer(
        question="What requires documented review?",
        context_text="Material changes require documented review.",
        policy_set="soc2",
    )

    assert "reviewed, tested, approved, and documented" in answer
    assert "retrieval logic" in answer


def test_clinical_safety_answer_mentions_escalation():
    answer = generate_answer(
        question="Should AI provide emergency medical guidance?",
        context_text="AI tools must not provide emergency medical guidance.",
        policy_set="clinical_safety",
    )

    assert "must not provide emergency medical guidance" in answer
    assert "qualified human review" in answer


def test_nist_answer_mentions_risk_governance():
    answer = generate_answer(
        question="How should AI risk be governed?",
        context_text="AI systems should use risk measurement and monitoring.",
        policy_set="nist_ai_rmf",
    )

    assert "risk measurement" in answer
    assert "human oversight" in answer
