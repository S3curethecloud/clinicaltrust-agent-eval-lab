
Architecture
Platform Name

ClinicalTrust Agent Evaluation Lab

Purpose

ClinicalTrust is a healthcare AI governance lab that demonstrates the journey from RAG to evaluation and evidence review.

The platform evaluates whether AI-generated answers are grounded, cited, policy-compliant, and ready for human review.

High-Level Flow
1. Ingest healthcare policy documents
2. Chunk and index documents
3. Retrieve relevant context
4. Generate an answer
5. Evaluate the answer
6. Produce governance evidence
7. Send the record to reviewer workflow
Main Components
RAG Layer

Responsible for document ingestion, chunking, retrieval, and citation metadata.

Agent Layer

Responsible for transforming a user question and retrieved context into a governed AI response.

Evaluation Layer

Scores the response using measurable criteria:

groundedness
relevance
citation coverage
hallucination risk
policy compliance
Governance Evidence Layer

Creates a durable evidence record for each run.

Reviewer Layer

Allows a human reviewer to approve, reject, or escalate an evaluated response.

Non-Goals

The lab does not implement:

runtime enforcement
production medical decisioning
patient diagnosis
protected health information processing
live authorization
secrets vault
OPA/Sentinel enforcement
