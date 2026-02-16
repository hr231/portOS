export default function RetroBtn({ children, onClick, t, active, style: s }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "4px 12px",
        fontFamily: "'Segoe UI', Tahoma, sans-serif",
        fontSize: 12,
        background: active ? t.surfaceLight : t.surface,
        color: t.text,
        border: "none",
        cursor: "pointer",
        boxShadow: active
          ? `inset 1px 1px 2px ${t.borderDarker}, inset -1px -1px 0 ${t.border}`
          : `1px 1px 0 ${t.borderDark}, -1px -1px 0 ${t.border}, inset 1px 1px 0 ${t.border}`,
        ...s,
      }}
    >
      {children}
    </button>
  );
}
