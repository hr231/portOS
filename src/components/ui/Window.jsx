import { useDrag } from "../../hooks/useDrag";

export default function Window({
  title,
  children,
  onClose,
  initialPos,
  zIndex,
  onFocus,
  t,
  isMobile,
}) {
  const { pos, onMouseDown } = useDrag(initialPos || { x: 80, y: 50 }, !isMobile);

  const wrapStyle = isMobile
    ? {
        position: "fixed",
        inset: 0,
        bottom: 52,
        zIndex: zIndex || 10,
        display: "flex",
        flexDirection: "column",
        background: t.surface,
      }
    : {
        position: "absolute",
        left: pos.x,
        top: pos.y,
        width: 560,
        maxWidth: "90vw",
        maxHeight: "78vh",
        zIndex: zIndex || 10,
        display: "flex",
        flexDirection: "column",
        background: t.surface,
        boxShadow: `3px 3px 0 ${t.borderDarker}`,
        border: `2px solid ${t.surface}`,
        borderTopColor: t.border,
        borderLeftColor: t.border,
        borderRightColor: t.borderDark,
        borderBottomColor: t.borderDark,
      };

  return (
    <div onClick={onFocus} style={wrapStyle}>
      {/* Title bar */}
      <div
        onMouseDown={onMouseDown}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "3px 4px",
          background: t.titleBar,
          cursor: isMobile ? "default" : "grab",
          userSelect: "none",
        }}
      >
        <span
          style={{
            fontFamily: "'Segoe UI', Tahoma, sans-serif",
            fontSize: 12,
            fontWeight: 700,
            color: t.titleBarText,
            paddingLeft: 4,
          }}
        >
          {title}
        </span>
        <div style={{ display: "flex", gap: 2 }}>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClose();
            }}
            style={{
              width: 20,
              height: 20,
              background: t.surface,
              border: `1px solid ${t.borderDark}`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 12,
              fontWeight: 700,
              cursor: "pointer",
              color: t.text,
              lineHeight: 1,
              boxShadow: `1px 1px 0 ${t.borderDark}, inset 1px 1px 0 ${t.border}`,
            }}
          >
            ✕
          </button>
        </div>
      </div>

      {/* Content area */}
      <div
        style={{
          flex: 1,
          overflow: "auto",
          padding: isMobile ? 16 : 20,
          background: t.cardBg,
          margin: 2,
          border: `1px solid ${t.borderDark}`,
          borderTopColor: t.borderDark,
          borderLeftColor: t.borderDark,
          borderRightColor: t.border,
          borderBottomColor: t.border,
        }}
      >
        {children}
      </div>
    </div>
  );
}
