import { experience } from "../../data/experience";

export default function ExperienceContent({ t }) {
  return (
    <div style={{ fontFamily: "'Segoe UI', Tahoma, sans-serif", color: t.text }}>
      {experience.map((e, i) => (
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
            <div>
              <span style={{ fontWeight: 700, fontSize: 14 }}>{e.role}</span>
              <span style={{ color: t.muted, fontSize: 13 }}>
                {" "}
                @ {e.company}
              </span>
            </div>
            <div style={{ textAlign: "right" }}>
              <span style={{ fontSize: 11, color: t.muted }}>{e.period}</span>
              {e.location && (
                <div style={{ fontSize: 10, color: t.muted }}>{e.location}</div>
              )}
            </div>
          </div>
          {e.highlights.map((h, j) => (
            <div
              key={j}
              style={{
                fontSize: 12,
                color: t.text,
                marginTop: 3,
                paddingLeft: 10,
                borderLeft: `2px solid ${t.tag}`,
              }}
            >
              {h}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
