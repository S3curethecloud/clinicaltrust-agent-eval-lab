import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";

function App() {
  const [records, setRecords] = useState([]);
  const [selected, setSelected] = useState(null);

  async function loadRecords() {
    const response = await fetch(`${API_BASE}/governance/evidence`);
    const data = await response.json();
    setRecords(data.records || []);
  }

  async function loadDetail(runId) {
    const response = await fetch(`${API_BASE}/governance/evidence/${runId}`);
    const data = await response.json();
    setSelected(data);
  }

  useEffect(() => {
    loadRecords();
  }, []);

  return (
    <main className="app">
      <section className="hero">
        <p className="eyebrow">ClinicalTrust Labs</p>
        <h1>Agent Evaluation Governance Console</h1>
        <p>
          Review RAG answers, evaluation scores, citations, hallucination risk,
          and governance evidence records before trust is granted.
        </p>
      </section>

      <section className="grid">
        <div className="panel">
          <div className="panelHeader">
            <h2>Evidence Runs</h2>
            <button onClick={loadRecords}>Refresh</button>
          </div>

          {records.length === 0 ? (
            <p className="muted">No evidence records found.</p>
          ) : (
            <div className="recordList">
              {records.map((record) => (
                <button
                  className="recordCard"
                  key={record.run_id}
                  onClick={() => loadDetail(record.run_id)}
                >
                  <strong>{record.question}</strong>
                  <span>Review: {record.reviewer_status}</span>
                  <span>Risk: {record.hallucination_risk}</span>
                  <span>Policy: {record.policy_compliance}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="panel detailPanel">
          <h2>Evidence Detail</h2>

          {!selected ? (
            <p className="muted">Select an evidence run to inspect details.</p>
          ) : (
            <div className="detail">
              <p className="runId">Run ID: {selected.run_id}</p>
              <h3>Question</h3>
              <p>{selected.question}</p>

              <h3>Answer</h3>
              <p>{selected.answer}</p>

              <h3>Scores</h3>
              <div className="scoreGrid">
                <span>Groundedness: {selected.scores?.groundedness}</span>
                <span>Relevance: {selected.scores?.relevance}</span>
                <span>Citations: {selected.scores?.citation_coverage}</span>
                <span>Risk: {selected.scores?.hallucination_risk}</span>
                <span>Policy: {selected.scores?.policy_compliance}</span>
                <span>Review: {selected.reviewer_status}</span>
              </div>

              <h3>Retrieved Context</h3>
              {selected.retrieved_chunks?.map((chunk) => (
                <div className="chunk" key={chunk.chunk_id}>
                  <strong>{chunk.chunk_id}</strong>
                  <p>{chunk.text}</p>
                  <small>{chunk.source}</small>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

export default App;
