from backend.app.evals.scorers import (
    classify_hallucination_risk,
    score_citation_coverage,
    score_groundedness,
)
from backend.app.schemas.evidence import RetrievedChunk


def test_groundedness_scores_overlap():
    chunks = [
        RetrievedChunk(
            chunk_id="c1",
            source="policy.md",
            text="Staff should avoid unnecessary patient identifiers in AI prompts.",
        )
    ]

    score = score_groundedness(
        "Staff should avoid patient identifiers in AI prompts.",
        chunks,
    )

    assert score > 0.5


def test_citation_coverage_requires_citations():
    assert score_citation_coverage("answer", ["policy.md"]) == 1.0
    assert score_citation_coverage("answer", []) == 0.0


def test_low_hallucination_requires_grounding_and_citations():
    assert classify_hallucination_risk(0.8, 1.0) == "LOW"
    assert classify_hallucination_risk(0.1, 0.0) == "HIGH"
