import { useState } from "react";

const contactInfo = [
  { icon: "✉️", val: "brahmbhatt.h@northeastern.edu" },
  { icon: "📞", val: "857-565-4643" },
  { icon: "📍", val: "Boston, MA" },
  { icon: "🔗", val: "linkedin.com/in/harshitb1611" },
];

export default function ContactContent({ t }) {
  const [sent, setSent] = useState(false);

  const inputStyle = {
    padding: "8px 10px",
    background: t.input,
    border: `1px solid ${t.borderDark}`,
    color: t.text,
    fontFamily: "'Segoe UI', Tahoma, sans-serif",
    fontSize: 13,
    outline: "none",
    width: "100%",
    boxSizing: "border-box",
    borderRadius: 2,
  };

  return (
    <div style={{ fontFamily: "'Segoe UI', Tahoma, sans-serif", color: t.text }}>
      {/* Contact cards */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8,
          marginBottom: 20,
        }}
      >
        {contactInfo.map((c, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              padding: "8px 12px",
              background: t.surfaceLight,
              borderRadius: 4,
              border: `1px solid ${t.border}`,
            }}
          >
            <span style={{ fontSize: 16 }}>{c.icon}</span>
            <span
              style={{
                fontSize: 13,
                color: t.accent,
                fontFamily: "monospace",
                wordBreak: "break-all",
              }}
            >
              {c.val}
            </span>
          </div>
        ))}
      </div>

      {/* Message form */}
      {!sent ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <input placeholder="Your name" style={inputStyle} />
          <input placeholder="Email" style={inputStyle} />
          <textarea
            placeholder="Message..."
            rows={3}
            style={{ ...inputStyle, resize: "vertical" }}
          />
          <button
            onClick={() => setSent(true)}
            style={{
              padding: "8px 16px",
              background: t.titleBar,
              color: t.titleBarText,
              border: "none",
              borderRadius: 2,
              fontFamily: "'Segoe UI', Tahoma, sans-serif",
              fontWeight: 700,
              fontSize: 13,
              cursor: "pointer",
              alignSelf: "flex-start",
              boxShadow: `1px 1px 0 ${t.borderDark}, inset 1px 1px 0 ${t.border}`,
            }}
          >
            Send Message
          </button>
        </div>
      ) : (
        <div
          style={{
            padding: 14,
            background: t.surfaceLight,
            borderRadius: 4,
            border: `1px solid ${t.tag}40`,
          }}
        >
          <span style={{ color: t.terminal, fontWeight: 700 }}>
            ✓ Message sent.
          </span>
          <div style={{ fontSize: 12, color: t.muted, marginTop: 4 }}>
            Harshit will respond within 24h.
          </div>
        </div>
      )}
    </div>
  );
}
