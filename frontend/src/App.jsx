import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_BASE = "http://localhost:8000";

function Badge({ children, tone = "neutral" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

function App() {
  const [records, setRecords] = useState([]);
  const [selected, setSelected] = useState(null);
  const [question, setQuestion] = useState("Can staff include patient identifiers in AI prompts?");
  const [isRunning, setIsRunning] = useState(false);
  const [analytics, setAnalytics] = useState(null);
  const [benchmark, setBenchmark] = useState(null);
  const [isBenchmarkRunning, setIsBenchmarkRunning] = useState(false);
  const [policySets, setPolicySets] = useState(["hipaa"]);
  const [policySet, setPolicySet] = useState("hipaa");
  const [exportResult, setExportResult] = useState(null);

  async function loadRecords() {
    const response = await fetch(`${API_BASE}/governance/evidence`);
    const data = await response.json();
    setRecords(data.records || []);
  }

  async function loadAnalytics() {
    const response = await fetch(`${API_BASE}/governance/analytics`);
    const data = await response.json();
    setAnalytics(data);
  }

  async function loadPolicySets() {
    const response = await fetch(`${API_BASE}/policy-sets`);
    const data = await response.json();
    setPolicySets(data.policy_sets || ["hipaa"]);
  }

  async function loadDetail(runId) {
    const response = await fetch(`${API_BASE}/governance/evidence/${runId}`);
    const data = await response.json();
    setSelected(data);
  }

  async function updateReviewStatus(status) {
    if (!selected?.run_id) return;

    await fetch(
      `${API_BASE}/reviewer/status?run_id=${selected.run_id}&status=${status}`,
      { method: "POST" }
    );

    await loadDetail(selected.run_id);
    await loadRecords();
    await loadAnalytics();
  }

  async function exportEvidence() {
    if (!selected?.run_id) return;

    const response = await fetch(
      `${API_BASE}/governance/evidence/${selected.run_id}/export`,
      { method: "POST" }
    );

    const data = await response.json();
    setExportResult(data);
  }

  async function runEvaluation(event) {
    event.preventDefault();

    const trimmed = question.trim();
    if (!trimmed) return;

    setIsRunning(true);

    try {
      const response = await fetch(
        `${API_BASE}/agent/respond?question=${encodeURIComponent(trimmed)}&policy_set=${encodeURIComponent(policySet)}`
      );
      const record = await response.json();
      setSelected(record);
      await loadRecords();
      await loadAnalytics();
    } finally {
      setIsRunning(false);
    }
  }

  async function runBenchmark() {
    setIsBenchmarkRunning(true);

    try {
      const response = await fetch(
        `${API_BASE}/benchmark/run?policy_set=${encodeURIComponent(policySet)}`,
        { method: "POST" }
      );
      const data = await response.json();
      setBenchmark(data);
      await loadRecords();
      await loadAnalytics();
    } finally {
      setIsBenchmarkRunning(false);
    }
  }

  useEffect(() => {
    loadRecords();
    loadAnalytics();
    loadPolicySets();
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

      <section className="runPanel">
        <div>
          <p className="eyebrow small">Run New Evaluation</p>
          <h2>Test a healthcare AI question</h2>
          <p>
            Generate a new governed agent response, score it, persist evidence,
            and route it for reviewer action.
          </p>
        </div>

        <form onSubmit={runEvaluation} className="runForm">
          <label className="policySelector">
            <span>Policy Set</span>
            <select value={policySet} onChange={(event) => setPolicySet(event.target.value)}>
              {policySets.map((item) => (
                <option key={item} value={item}>
                  {item.replaceAll("_", " ").toUpperCase()}
                </option>
              ))}
            </select>
          </label>

          <input
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a healthcare policy question..."
          />
          <button type="submit" disabled={isRunning}>
            {isRunning ? "Running..." : "Run Evaluation"}
          </button>
        </form>
      </section>

      <section className="benchmarkPanel">
        <div>
          <p className="eyebrow small">Benchmark Suite</p>
          <h2>Run evaluation set</h2>
          <p>
            Execute the healthcare policy question set and generate governed
            evidence records automatically.
          </p>
        </div>

        <button onClick={runBenchmark} disabled={isBenchmarkRunning}>
          {isBenchmarkRunning ? "Running Benchmark..." : "Run Benchmark"}
        </button>

        {benchmark && (
          <div className="benchmarkResults">
            <span>Questions: {benchmark.total_questions}</span>
            <span>Avg Groundedness: {benchmark.average_groundedness}</span>
            <span>Avg Relevance: {benchmark.average_relevance}</span>
          </div>
        )}
      </section>

      <section className="metrics">
        <div className="metricCard">
          <span>Total Runs</span>
          <strong>{analytics?.total_runs ?? metrics.total}</strong>
        </div>
        <div className="metricCard">
          <span>Approval Rate</span>
          <strong>{Math.round((analytics?.rates?.approval_rate ?? 0) * 100)}%</strong>
        </div>
        <div className="metricCard">
          <span>Avg Groundedness</span>
          <strong>{analytics?.averages?.groundedness ?? "0.00"}</strong>
        </div>
        <div className="metricCard">
          <span>High Risk</span>
          <strong>{analytics?.risk_distribution?.high ?? metrics.highRisk}</strong>
        </div>
      </section>

      <section className="analyticsGrid">
        <div className="analyticsCard">
          <h3>Review Status</h3>
          <p>Approved: {analytics?.review_status?.approved ?? 0}</p>
          <p>Rejected: {analytics?.review_status?.rejected ?? 0}</p>
          <p>Escalated: {analytics?.review_status?.escalated ?? 0}</p>
          <p>Pending: {analytics?.review_status?.pending ?? 0}</p>
        </div>

        <div className="analyticsCard">
          <h3>Risk Distribution</h3>
          <p>Low: {analytics?.risk_distribution?.low ?? 0}</p>
          <p>Medium: {analytics?.risk_distribution?.medium ?? 0}</p>
          <p>High: {analytics?.risk_distribution?.high ?? 0}</p>
        </div>

        <div className="analyticsCard">
          <h3>Policy Distribution</h3>
          <p>Pass: {analytics?.policy_distribution?.pass ?? 0}</p>
          <p>Warn: {analytics?.policy_distribution?.warn ?? 0}</p>
          <p>Fail: {analytics?.policy_distribution?.fail ?? 0}</p>
        </div>

        <div className="analyticsCard">
          <h3>Average Scores</h3>
          <p>Groundedness: {analytics?.averages?.groundedness ?? 0}</p>
          <p>Relevance: {analytics?.averages?.relevance ?? 0}</p>
          <p>Citation Coverage: {analytics?.averages?.citation_coverage ?? 0}</p>
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

              <h3>Governance Decision</h3>
              <div className={`governanceDecision ${selected.governance_decision?.decision?.toLowerCase() || "warn"}`}>
                <strong>{selected.governance_decision?.decision || "PENDING"}</strong>
                <ul>
                  {selected.governance_decision?.reasons?.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>
              </div>

              {selected.retrieved_chunks?.length === 0 && (
                <div className="noEvidenceWarning">
                  ⚠ No policy evidence retrieved. Approval is blocked until grounded evidence is available.
                </div>
              )}

              <h3>Reviewer Actions</h3>
              <div className="reviewActions">
                <button
                  className="approve"
                  disabled={!selected.governance_decision?.approval_allowed}
                  onClick={() => updateReviewStatus("APPROVED")}
                >
                  Approve
                </button>
                <button className="reject" onClick={() => updateReviewStatus("REJECTED")}>
                  Reject
                </button>
                <button className="escalate" onClick={() => updateReviewStatus("ESCALATED")}>
                  Escalate
                </button>
                <button className="exportEvidence" onClick={exportEvidence}>
                  Export Evidence
                </button>
              </div>

              {exportResult?.exported && (
                <div className="exportResult">
                  <strong>Auditor package exported</strong>
                  <code>{exportResult.path}</code>
                </div>
              )}

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
