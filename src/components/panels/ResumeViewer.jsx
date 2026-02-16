import { useState, useRef, useCallback } from "react";

export default function ResumeViewer({ t }) {
  const [zoom, setZoom] = useState(100);
  const [page] = useState(1);
  const paperRef = useRef(null);

  // ── Print: opens a new window with the resume paper and triggers print ──
  const handlePrint = useCallback(() => {
    const paperEl = paperRef.current;
    if (!paperEl) return;
    const printWin = window.open("", "_blank", "width=700,height=900");
    if (!printWin) return;
    printWin.document.write(`
      <!DOCTYPE html>
      <html><head><title>Harshit_B_Resume</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { display: flex; justify-content: center; padding: 0; }
        @media print { body { padding: 0; } }
      </style>
      </head><body>${paperEl.outerHTML}</body></html>
    `);
    printWin.document.close();
    printWin.focus();
    setTimeout(() => printWin.print(), 300);
  }, []);

  // ── Save: renders the resume HTML as a downloadable .html file ──
  const handleSave = useCallback(() => {
    const paperEl = paperRef.current;
    if (!paperEl) return;
    const html = `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Harshit_B_Resume</title>
<style>* { margin:0; padding:0; box-sizing:border-box; } body { display:flex; justify-content:center; padding:24px; font-family:'Times New Roman',Times,serif; }</style>
</head><body>${paperEl.outerHTML}</body></html>`;
    const blob = new Blob([html], { type: "text/html" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "Harshit_B_Resume.html";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, []);

  const toolBtnStyle = {
    padding: "2px 8px",
    background: t.surface,
    border: `1px solid ${t.borderDark}`,
    color: t.text,
    fontFamily: "'Segoe UI', Tahoma, sans-serif",
    fontSize: 11,
    cursor: "pointer",
    boxShadow: `1px 1px 0 ${t.borderDark}, inset 1px 1px 0 ${t.border}`,
  };

  const secTitle = {
    fontSize: 10,
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: 1.5,
    color: "#555",
    borderBottom: "1.5px solid #222",
    paddingBottom: 3,
    marginBottom: 6,
    marginTop: 14,
  };

  const bullet = {
    fontSize: 10.5,
    color: "#222",
    lineHeight: 1.5,
    marginBottom: 2,
    paddingLeft: 10,
    textIndent: -10,
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        fontFamily: "'Segoe UI', Tahoma, sans-serif",
      }}
    >
      {/* Toolbar */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 4,
          padding: "4px 6px",
          flexWrap: "wrap",
          background: t.surface,
          borderBottom: `1px solid ${t.borderDark}`,
          marginBottom: 8,
        }}
      >
        <div style={{ flex: 1 }} />
        <button
          style={toolBtnStyle}
          onClick={() => setZoom((z) => Math.max(60, z - 10))}
        >
          −
        </button>
        <span
          style={{
            fontSize: 11,
            color: t.text,
            minWidth: 36,
            textAlign: "center",
            fontFamily: "monospace",
          }}
        >
          {zoom}%
        </span>
        <button
          style={toolBtnStyle}
          onClick={() => setZoom((z) => Math.min(150, z + 10))}
        >
          +
        </button>
        <div
          style={{
            width: 1,
            height: 18,
            background: t.borderDark,
            margin: "0 6px",
          }}
        />
        <button
          style={{ ...toolBtnStyle, fontWeight: 700 }}
          onClick={handlePrint}
        >
          🖨️ Print
        </button>
        <button
          style={{ ...toolBtnStyle, fontWeight: 700 }}
          onClick={handleSave}
        >
          💾 Save
        </button>
      </div>

      {/* Page status */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 8,
          marginBottom: 6,
        }}
      >
        <span style={{ fontSize: 10, color: t.muted }}>Page {page} of 1</span>
        <span style={{ fontSize: 10, color: t.muted }}>|</span>
        <span style={{ fontSize: 10, color: t.muted }}>
          Harshit_B_Resume.pdf
        </span>
      </div>

      {/* Paper */}
      <div
        style={{
          flex: 1,
          overflow: "auto",
          display: "flex",
          justifyContent: "center",
          padding: "0 4px 16px",
        }}
      >
        <div
          ref={paperRef}
          style={{
            width: 540,
            minHeight: 720,
            background: "#ffffff",
            color: "#000",
            padding: "36px 40px",
            boxShadow: `4px 4px 0 ${t.borderDarker}, 2px 2px 0 ${t.borderDark}`,
            border: "1px solid #999",
            transform: `scale(${zoom / 100})`,
            transformOrigin: "top center",
            fontFamily: "'Times New Roman', Times, serif",
          }}
        >
          {/* ── Header ── */}
          <div
            style={{
              textAlign: "center",
              marginBottom: 10,
              borderBottom: "2px solid #000",
              paddingBottom: 10,
            }}
          >
            <div
              style={{
                fontSize: 22,
                fontWeight: 700,
                letterSpacing: 2,
                textTransform: "uppercase",
              }}
            >
              Harshit B.
            </div>
            <div
              style={{
                fontSize: 10,
                color: "#444",
                marginTop: 4,
                fontFamily: "'Courier New', monospace",
              }}
            >
              Boston, MA &nbsp;·&nbsp; 857-565-4643 &nbsp;·&nbsp;
              brahmbhatt.h@northeastern.edu &nbsp;·&nbsp; LinkedIn: /in/harshitb1611
            </div>
          </div>

          {/* ── Education ── */}
          <div style={secTitle}>Education</div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 11,
            }}
          >
            <div>
              <b>Master of Science in Data Analytics Engineering</b> —
              Northeastern University
            </div>
            <div style={{ color: "#555", whiteSpace: "nowrap" }}>Dec 2026</div>
          </div>
          <div style={{ fontSize: 10, color: "#555" }}>
            GPA: 3.9/4.0 &nbsp;·&nbsp; Boston, MA
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 11,
              marginTop: 4,
            }}
          >
            <div>
              <b>Bachelor of Engineering in Computer Engineering</b> — LDRP
              Institute of Technology
            </div>
            <div style={{ color: "#555", whiteSpace: "nowrap" }}>May 2024</div>
          </div>
          <div style={{ fontSize: 10, color: "#555" }}>
            GPA: 3.3/4.0 &nbsp;·&nbsp; Gandhinagar, India
          </div>

          {/* ── Work Experience ── */}
          <div style={secTitle}>Work Experience</div>

          {/* Staples */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 11,
            }}
          >
            <div>
              <b>AI Engineer Intern</b> — Staples Inc.
            </div>
            <div style={{ color: "#555", whiteSpace: "nowrap" }}>
              Jan 2026 – Present
            </div>
          </div>
          <div style={{ fontSize: 10, color: "#555", marginBottom: 2 }}>
            Framingham, MA
          </div>
          <div style={bullet}>
            • Spearheaded production-grade LLM applications automating high-labor
            workflows, reducing manual effort by 40% and error rates across
            enterprise retail operations.
          </div>
          <div style={bullet}>
            • Constructed LangGraph-based inference pipelines with FastAPI,
            GraphQL, and gRPC integrations for real-time reasoning and retrieval
            over PGVector and Neo4j.
          </div>
          <div style={bullet}>
            • Integrated OpenAI, Anthropic, Ollama, and vLLM backends through
            unified connector APIs, enabling rapid experimentation and model
            portability.
          </div>
          <div style={bullet}>
            • Optimized Kubernetes-deployed vLLM clusters for low latency and
            high throughput via dynamic batching, quantization, and GPU
            utilization tuning.
          </div>

          {/* Pixeltechnologies */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 11,
              marginTop: 8,
            }}
          >
            <div>
              <b>ML Engineer Intern</b> — Pixeltechnologies
            </div>
            <div style={{ color: "#555", whiteSpace: "nowrap" }}>
              Jan – Jul 2024
            </div>
          </div>
          <div style={bullet}>
            • Architected Python prediction pipelines using scikit-learn and
            XGBoost for 100K+ events; enhanced campaign ROI by 22%.
          </div>
          <div style={bullet}>
            • Engineered SQL-driven ETL and Airflow DAGs to process
            high-velocity A/B test logs; cut model retraining latency by 40%.
          </div>
          <div style={bullet}>
            • Operationalized ML explainability by deploying interpretable models
            with SHAP values; uncovered 3 key vulnerabilities and improved
            accuracy by 18%.
          </div>

          {/* GROWITUP */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              fontSize: 11,
              marginTop: 8,
            }}
          >
            <div>
              <b>Data Analyst Intern</b> — GROWITUP
            </div>
            <div style={{ color: "#555", whiteSpace: "nowrap" }}>
              Jul 2023 – Jan 2024
            </div>
          </div>
          <div style={bullet}>
            • Pioneered a vectorized search system using OpenAI embeddings and
            FastAPI, achieving 96% faster retrieval across 5K+ documents.
          </div>
          <div style={bullet}>
            • Modeled user sessions with Snowflake and PostgreSQL to detect
            behavioral anomalies and data drift patterns.
          </div>

          {/* ── Projects ── */}
          <div style={secTitle}>Projects</div>
          <div style={{ fontSize: 11 }}>
            <b>FrontShiftAI: Multi-Tenant Agentic Platform</b>{" "}
            <span style={{ color: "#666", fontSize: 10 }}>
              | FastAPI, Airflow, ChromaDB, Modal, LiveKit, React
            </span>
          </div>
          <div style={bullet}>
            • Designed a Unified Agent Router in FastAPI using regex-based intent
            detection with LLM fallback to intelligently route requests between
            deterministic SQL agents and probabilistic LLaMA-3 RAG pipelines.
          </div>
          <div style={bullet}>
            • Automated Airflow 3.0 ETL pipelines utilizing a dedicated SmolVLM
            Vision Microservice to ingest unstructured PDF data, validating
            quality via Great Expectations before embedding into vector databases.
          </div>
          <div style={bullet}>
            • Implemented Hybrid Search (BM25 + Vector) with Cross-Encoder
            Reranking, significantly reducing hallucination rates for policy
            queries.
          </div>

          <div style={{ fontSize: 11, marginTop: 6 }}>
            <b>Credit Risk Forecasting via Temporal Architectures</b>{" "}
            <span style={{ color: "#666", fontSize: 10 }}>
              | TensorFlow, SHAP, Azure CI/CD, SQL
            </span>
          </div>
          <div style={bullet}>
            • Segmented 30K+ financial transactions into lag-aware bins and
            extracted temporal features to surface default patterns.
          </div>
          <div style={bullet}>
            • Trained Bi-LSTM and TabTransformer models for risk classification;
            boosted minority F1-score by 16% achieving 81.9% accuracy.
          </div>
          <div style={bullet}>
            • Visualized temporal risk triggers using SHAP plots to improve
            auditor interpretability and model trust.
          </div>

          {/* ── Technical Skills ── */}
          <div style={secTitle}>Technical Skills</div>
          <div style={{ fontSize: 10, lineHeight: 1.7, color: "#222" }}>
            <b>Languages:</b> Python, C++, SQL, Shell Scripting, JavaScript
            &nbsp;&nbsp;
            <b>AI/ML/DL:</b> Scikit-learn, XGBoost, TensorFlow, PyTorch, Hugging
            Face, SHAP, Model Training & Fine-Tuning &nbsp;&nbsp;
            <b>LLM & Gen AI:</b> OpenAI API, LangChain, LangGraph, vLLM, RAG
            Pipelines, Agentic Frameworks, Tool-Calling &nbsp;&nbsp;
            <b>Vector DBs:</b> ChromaDB, Pinecone, PGVector, Neo4j, Hybrid
            Search (BM25 + Vector) &nbsp;&nbsp;
            <b>MLOps:</b> Apache Airflow, FastAPI, Docker, Kubernetes, CI/CD
            (Azure, GitHub), Model Monitoring &nbsp;&nbsp;
            <b>Cloud:</b> GCP (GKE, Cloud SQL), AWS S3, Snowflake, PostgreSQL,
            Azure Databricks
          </div>

          {/* Footer watermark */}
          <div
            style={{
              marginTop: 20,
              textAlign: "center",
              fontSize: 9,
              color: "#bbb",
              fontFamily: "'Courier New', monospace",
              borderTop: "1px solid #ddd",
              paddingTop: 8,
            }}
          >
            Rendered in HarshitOS Document Viewer v1.0 &nbsp;·&nbsp; Page 1 of
            1
          </div>
        </div>
      </div>
    </div>
  );
}
