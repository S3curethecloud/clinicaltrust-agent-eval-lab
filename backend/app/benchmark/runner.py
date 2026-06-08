import json
from pathlib import Path

from backend.app.agent.response_agent import create_agent_response
from backend.app.governance.evidence_store import save_evidence_record


EVAL_FILE = Path("data/eval_sets/sample_questions.json")


def run_benchmark() -> list[dict]:
    questions = json.loads(EVAL_FILE.read_text(encoding="utf-8"))

    results: list[dict] = []

    for item in questions:
        record = create_agent_response(item["question"])
        save_evidence_record(record)

        results.append(
            {
                "run_id": record.run_id,
                "question": record.question,
                "groundedness": record.scores.groundedness,
                "relevance": record.scores.relevance,
                "citation_coverage": record.scores.citation_coverage,
                "policy": record.scores.policy_compliance,
                "risk": record.scores.hallucination_risk,
                "reviewer_status": record.reviewer_status,
            }
        )

    return results
