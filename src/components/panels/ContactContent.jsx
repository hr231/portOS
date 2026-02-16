export default function ContactContent({ t }) {
  const links = [
    {
      icon: "✉️",
      label: "Email",
      val: "brahmbhatt.h@northeastern.edu",
      href: "mailto:brahmbhatt.h@northeastern.edu",
    },
    {
      icon: "📞",
      label: "Phone",
      val: "857-565-4643",
      href: "tel:+18575654643",
    },
    {
      icon: "🔗",
      label: "LinkedIn",
      val: "linkedin.com/in/harshitb1611",
      href: "https://linkedin.com/in/harshitb1611",
    },
    {
      icon: "🐙",
      label: "GitHub",
      val: "github.com/harshitb",
      href: "https://github.com/harshitb",
    },
    {
      icon: "📍",
      label: "Location",
      val: "Boston, MA",
      href: null,
    },
  ];

  return (
    <div
      style={{
        fontFamily: "'Segoe UI', Tahoma, sans-serif",
        color: t.text,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 8,
        }}
      >
        {links.map((c, i) => {
          const inner = (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                padding: "10px 14px",
                background: t.surfaceLight,
                borderRadius: 4,
                border: `1px solid ${t.border}`,
                transition: "border-color 0.15s",
                cursor: c.href ? "pointer" : "default",
              }}
            >
              <span style={{ fontSize: 18 }}>{c.icon}</span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div
                  style={{
                    fontSize: 11,
                    color: t.muted,
                    marginBottom: 2,
                    fontWeight: 600,
                  }}
                >
                  {c.label}
                </div>
                <span
                  style={{
                    fontSize: 13,
                    color: c.href ? t.accent : t.text,
                    fontFamily: "monospace",
                    wordBreak: "break-all",
                  }}
                >
                  {c.val}
                </span>
              </div>
              {c.href && (
                <span style={{ fontSize: 12, color: t.muted }}>↗</span>
              )}
            </div>
          );

          if (c.href) {
            return (
              <a
                key={i}
                href={c.href}
                target={c.href.startsWith("http") ? "_blank" : undefined}
                rel="noopener noreferrer"
                style={{ textDecoration: "none" }}
              >
                {inner}
              </a>
            );
          }
          return <div key={i}>{inner}</div>;
        })}
      </div>

      {/* Terminal-style hint */}
      <div
        style={{
          marginTop: 16,
          padding: "8px 14px",
          background: t.terminalBg,
          borderRadius: 4,
          border: `1px solid ${t.borderDark}`,
          fontFamily: "monospace",
          fontSize: 11,
          color: t.terminal,
        }}
      >
        $ echo "Preferred contact: email or LinkedIn"
      </div>
    </div>
  );
}
