import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";

function Badge({ children, tone = "neutral" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

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

  const metrics = useMemo(() => {
    const total = records.length;
    const approved = records.filter((r) => r.reviewer_status === "APPROVED").length;
    const highRisk = records.filter((r) => r.hallucination_risk === "HIGH").length;
    const pending = records.filter((r) => r.reviewer_status === "PENDING").length;

    return { total, approved, highRisk, pending };
  }, [records]);

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

      <section className="metrics">
        <div className="metricCard">
          <span>Total Runs</span>
          <strong>{metrics.total}</strong>
        </div>
        <div className="metricCard">
          <span>Approved</span>
          <strong>{metrics.approved}</strong>
        </div>
        <div className="metricCard">
          <span>High Risk</span>
          <strong>{metrics.highRisk}</strong>
        </div>
        <div className="metricCard">
          <span>Pending Review</span>
          <strong>{metrics.pending}</strong>
        </div>
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
                  className={`recordCard ${selected?.run_id === record.run_id ? "active" : ""}`}
                  key={record.run_id}
                  onClick={() => loadDetail(record.run_id)}
                >
                  <strong>{record.question}</strong>
                  <small>ID: {record.run_id.slice(0, 8)}</small>
                  <div className="badgeRow">
                    <Badge tone={record.reviewer_status === "APPROVED" ? "good" : "warn"}>
                      {record.reviewer_status}
                    </Badge>
                    <Badge tone={record.hallucination_risk === "LOW" ? "good" : "bad"}>
                      Risk: {record.hallucination_risk}
                    </Badge>
                    <Badge tone={record.policy_compliance === "PASS" ? "good" : "bad"}>
                      Policy: {record.policy_compliance}
                    </Badge>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="panel detailPanel">
          <div className="panelHeader">
            <h2>Evidence Detail</h2>
            {selected && <Badge tone="good">{selected.reviewer_status}</Badge>}
          </div>

          {!selected ? (
            <p className="muted">Select an evidence run to inspect details.</p>
          ) : (
            <div className="detail">
              <p className="runId">Run ID: {selected.run_id}</p>

              <h3>Question</h3>
              <p>{selected.question}</p>

              <h3>Answer</h3>
              <p>{selected.answer}</p>

              <h3>Evaluation Scores</h3>
              <div className="scoreGrid">
                <div><span>Groundedness</span><strong>{selected.scores?.groundedness}</strong></div>
                <div><span>Relevance</span><strong>{selected.scores?.relevance}</strong></div>
                <div><span>Citation Coverage</span><strong>{selected.scores?.citation_coverage}</strong></div>
                <div><span>Hallucination Risk</span><strong>{selected.scores?.hallucination_risk}</strong></div>
                <div><span>Policy Compliance</span><strong>{selected.scores?.policy_compliance}</strong></div>
                <div><span>Reviewer Status</span><strong>{selected.reviewer_status}</strong></div>
              </div>

              <h3>Citations</h3>
              <div className="citationList">
                {selected.citations?.map((citation, index) => (
                  <code key={`${citation}-${index}`}>{citation}</code>
                ))}
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
