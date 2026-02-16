export default function Tag({ children, t }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "1px 7px",
        borderRadius: 2,
        fontSize: 11,
        background: t.tagBg,
        color: t.tag,
        fontFamily: "monospace",
        marginRight: 4,
        marginBottom: 4,
      }}
    >
      {children}
    </span>
  );
}
