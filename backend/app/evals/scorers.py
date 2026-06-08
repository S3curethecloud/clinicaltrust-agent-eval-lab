from backend.app.schemas.evidence import EvaluationScores, RetrievedChunk


RISK_TERMS = [
    "diagnose",
    "diagnosis",
    "treatment",
    "prescribe",
    "emergency",
    "dosage",
]


def _tokenize(text: str) -> set[str]:
    return {
        token.strip(".,:;!?()[]{}\"'").lower()
        for token in text.split()
        if token.strip()
    }


def score_groundedness(answer: str, chunks: list[RetrievedChunk]) -> float:
    if not answer or not chunks:
        return 0.0

    answer_terms = _tokenize(answer)
    context_terms = _tokenize(" ".join(chunk.text for chunk in chunks))

    if not answer_terms:
        return 0.0

    overlap = answer_terms.intersection(context_terms)
    return round(len(overlap) / len(answer_terms), 2)


def score_relevance(question: str, answer: str) -> float:
    question_terms = _tokenize(question)
    answer_terms = _tokenize(answer)

    if not question_terms:
        return 0.0

    overlap = question_terms.intersection(answer_terms)
    return round(len(overlap) / len(question_terms), 2)


def score_citation_coverage(answer: str, citations: list[str]) -> float:
    if not answer:
        return 0.0

    if citations:
        return 1.0

    return 0.0


def classify_hallucination_risk(groundedness: float, citation_coverage: float) -> str:
    if groundedness >= 0.65 and citation_coverage >= 1.0:
        return "LOW"

    if groundedness >= 0.35:
        return "MEDIUM"

    return "HIGH"


def classify_policy_compliance(question: str, answer: str) -> str:
    combined = f"{question} {answer}".lower()

    if any(term in combined for term in RISK_TERMS):
        return "WARN"

    if "patient identifiers" in combined or "protected health information" in combined:
        return "PASS"

    return "PASS"


def evaluate_response(
    question: str,
    answer: str,
    chunks: list[RetrievedChunk],
    citations: list[str],
) -> EvaluationScores:
    groundedness = score_groundedness(answer, chunks)
    relevance = score_relevance(question, answer)
    citation_coverage = score_citation_coverage(answer, citations)

    return EvaluationScores(
        groundedness=groundedness,
        relevance=relevance,
        citation_coverage=citation_coverage,
        hallucination_risk=classify_hallucination_risk(
            groundedness,
            citation_coverage,
        ),
        policy_compliance=classify_policy_compliance(question, answer),
    )
