import { skills } from "../../data/skills";
import Tag from "../ui/Tag";

export default function AboutContent({ t }) {
  return (
    <div
      style={{
        fontFamily: "'Segoe UI', Tahoma, sans-serif",
        color: t.text,
        lineHeight: 1.7,
      }}
    >
      {/* Profile header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
          marginBottom: 16,
          flexWrap: "wrap",
        }}
      >
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: 4,
            background: t.titleBar,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 24,
            fontWeight: 700,
            color: t.titleBarText,
          }}
        >
          H
        </div>
        <div>
          <div style={{ fontSize: 18, fontWeight: 700, color: t.text }}>
            Harshit B.
          </div>
          <div style={{ fontSize: 12, color: t.muted }}>
            AI Engineer · ML Systems · Boston, MA
          </div>
          <div style={{ fontSize: 11, color: t.muted }}>
            MS Data Analytics — Northeastern (3.9 GPA)
          </div>
        </div>
      </div>

      <p style={{ fontSize: 13, color: t.text, margin: "0 0 16px" }}>
        I build production ML systems — agentic AI platforms, temporal risk
        models, real-time voice agents, and scalable data pipelines. I care
        about systems that work at scale, not just in notebooks.
      </p>

      {/* Certifications terminal block */}
      <div
        style={{
          padding: 10,
          background: t.terminalBg,
          borderRadius: 4,
          border: `1px solid ${t.borderDark}`,
          marginBottom: 16,
        }}
      >
        <div
          style={{ fontFamily: "monospace", fontSize: 11, color: t.terminal }}
        >
          $ cat certifications.txt
        </div>
        <div
          style={{
            fontFamily: "monospace",
            fontSize: 11,
            color: "#ccc",
            marginTop: 4,
          }}
        >
          Stanford ML · DeepLearning.AI GenAI · UPenn Quant Modeling
        </div>
      </div>

      {/* Skills by category */}
      {Object.entries(skills).map(([cat, items]) => (
        <div key={cat} style={{ marginBottom: 8 }}>
          <div
            style={{ fontSize: 12, fontWeight: 700, color: t.muted, marginBottom: 4 }}
          >
            {cat}
          </div>
          <div style={{ display: "flex", flexWrap: "wrap" }}>
            {items.map((s) => (
              <Tag key={s} t={t}>
                {s}
              </Tag>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
