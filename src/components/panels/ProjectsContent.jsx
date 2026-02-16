import { projects } from "../../data/projects";
import Tag from "../ui/Tag";

export default function ProjectsContent({ t }) {
  return (
    <div style={{ fontFamily: "'Segoe UI', Tahoma, sans-serif", color: t.text }}>
      {projects.map((p, i) => (
        <div
          key={i}
          style={{
            padding: 14,
            marginBottom: 10,
            background: t.surfaceLight,
            borderRadius: 4,
            border: `1px solid ${t.border}`,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              flexWrap: "wrap",
              marginBottom: 6,
            }}
          >
            <span style={{ fontWeight: 700, fontSize: 14, color: t.accent }}>
              {p.name}
            </span>
            <span style={{ fontSize: 11, color: t.muted }}>{p.date}</span>
          </div>
          <div style={{ marginBottom: 6, display: "flex", flexWrap: "wrap" }}>
            {p.tags.map((x) => (
              <Tag key={x} t={t}>
                {x}
              </Tag>
            ))}
          </div>
          <p style={{ fontSize: 12, color: t.text, margin: 0, lineHeight: 1.6 }}>
            {p.desc}
          </p>
        </div>
      ))}
    </div>
  );
}
