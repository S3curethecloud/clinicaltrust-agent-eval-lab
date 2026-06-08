from pydantic import BaseModel
from typing import List, Literal


ReviewerStatus = Literal["PENDING", "APPROVED", "REJECTED", "ESCALATED"]


class RetrievedChunk(BaseModel):
    chunk_id: str
    source: str
    text: str


class EvaluationScores(BaseModel):
    groundedness: float
    relevance: float
    citation_coverage: float
    hallucination_risk: Literal["LOW", "MEDIUM", "HIGH"]
    policy_compliance: Literal["PASS", "WARN", "FAIL"]


class EvidenceRecord(BaseModel):
    run_id: str
    question: str
    retrieved_chunks: List[RetrievedChunk]
    answer: str
    citations: List[str]
    scores: EvaluationScores
    reviewer_status: ReviewerStatus = "PENDING"
