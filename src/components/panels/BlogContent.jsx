export default function BlogContent({ t }) {
  return (
    <div
      style={{
        fontFamily: "'Segoe UI', Tahoma, sans-serif",
        color: t.text,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: 220,
        textAlign: "center",
        gap: 12,
      }}
    >
      <div style={{ fontSize: 40 }}>📝</div>
      <div style={{ fontSize: 16, fontWeight: 700, color: t.text }}>
        Blog — Coming Soon
      </div>
      <p
        style={{
          fontSize: 13,
          color: t.muted,
          maxWidth: 340,
          lineHeight: 1.6,
          margin: 0,
        }}
      >
        Posts on ML systems, LLM engineering, and lessons from building
        production AI are on the way. Stay tuned!
      </p>
      <div
        style={{
          marginTop: 8,
          padding: "8px 16px",
          background: t.terminalBg,
          borderRadius: 4,
          border: `1px solid ${t.borderDark}`,
          fontFamily: "monospace",
          fontSize: 11,
          color: t.terminal,
        }}
      >
        $ echo "blog posts" &gt;&gt; /dev/future
      </div>
    </div>
  );
}
