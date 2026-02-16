import { useState, useRef, useEffect } from "react";
import { bootLines } from "../../data/bootLines";
import { skills } from "../../data/skills";

export default function TerminalContent({ t, onCommand }) {
  const [lines, setLines] = useState([]);
  const [input, setInput] = useState("");
  const [bootDone, setBootDone] = useState(false);
  const bottomRef = useRef(null);

  // Boot sequence animation
  useEffect(() => {
    let i = 0;
    const iv = setInterval(() => {
      if (i < bootLines.length) {
        setLines((prev) => [...prev, bootLines[i]]);
        i++;
      } else {
        clearInterval(iv);
        setBootDone(true);
      }
    }, 120);
    return () => clearInterval(iv);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [lines]);

  const handleKey = (e) => {
    if (e.key !== "Enter" || !input.trim()) return;
    const cmd = input.trim().toLowerCase();
    setLines((prev) => [...prev, `harshit@os:~$ ${input}`]);

    const cmds = {
      help: "Commands: about, projects, experience, blog, contact, skills, theme, clear",
      skills: Object.entries(skills)
        .map(([k, v]) => `  ${k}: ${v.join(", ")}`)
        .join("\n"),
      clear: null,
    };

    if (cmds[cmd] !== undefined) {
      if (cmd === "clear") setLines([]);
      else setLines((prev) => [...prev, cmds[cmd]]);
    } else if (
      ["about", "projects", "experience", "blog", "contact"].includes(cmd)
    ) {
      onCommand(cmd);
      setLines((prev) => [...prev, `Opening ${cmd}...`]);
    } else if (cmd === "theme") {
      onCommand("__theme");
      setLines((prev) => [...prev, "Theme toggled."]);
    } else {
      setLines((prev) => [
        ...prev,
        `command not found: ${cmd}. Type 'help'`,
      ]);
    }
    setInput("");
  };

  return (
    <div
      style={{
        background: t.terminalBg,
        padding: 12,
        borderRadius: 2,
        minHeight: 200,
        fontFamily: "monospace",
        fontSize: 12,
        lineHeight: 1.6,
      }}
    >
      {lines.map((l, i) => {
        const line = l || "";
        let color = "#aaa";
        if (line.startsWith("[OK]")) color = t.terminal;
        else if (line.startsWith("harshit@")) color = "#00bfff";
        else if (line.startsWith("command not found")) color = "#ff6b6b";
        return (
          <div key={i} style={{ color, whiteSpace: "pre-wrap" }}>
            {line || "\u00A0"}
          </div>
        );
      })}
      {bootDone && (
        <div style={{ display: "flex", alignItems: "center" }}>
          <span style={{ color: "#00bfff" }}>harshit@os:~$&nbsp;</span>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            style={{
              background: "transparent",
              border: "none",
              color: "#e0e0e0",
              fontFamily: "monospace",
              fontSize: 12,
              outline: "none",
              flex: 1,
            }}
            autoFocus
          />
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}
