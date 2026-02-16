import { useState } from "react";

export default function DesktopIcon({ icon, label, onClick, t }) {
  const [hover, setHover] = useState(false);

  return (
    <div
      onClick={onClick}
      onDoubleClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 4,
        cursor: "pointer",
        padding: 8,
        borderRadius: 2,
        width: 76,
        background: hover ? `${t.accent}22` : "transparent",
        transition: "background 0.15s",
      }}
    >
      <div style={{ fontSize: 30 }}>{icon}</div>
      <span
        style={{
          fontFamily: "'Segoe UI', Tahoma, sans-serif",
          fontSize: 11,
          textAlign: "center",
          color: t.titleBarText,
          textShadow:
            t.bg === "#008080" ? "1px 1px 2px rgba(0,0,0,0.7)" : "none",
          wordBreak: "break-word",
          lineHeight: 1.2,
        }}
      >
        {label}
      </span>
    </div>
  );
}
