import { useState, useRef, useEffect, useCallback } from "react";
import { bootLines } from "../../data/bootLines";
import { skills } from "../../data/skills";
import { API_URL } from "../../config";

export default function TerminalContent({ t, onCommand }) {
  const [lines, setLines] = useState([]);
  const [input, setInput] = useState("");
  const [bootDone, setBootDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

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

  // Focus input after loading completes
  useEffect(() => {
    if (!loading && bootDone) {
      inputRef.current?.focus();
    }
  }, [loading, bootDone]);

  // Ask the AI agent via the backend
  const askAgent = useCallback(async (question) => {
    setLoading(true);
    setLines((prev) => [...prev, { text: "[querying knowledge graph...]", type: "loading" }]);

    try {
      const res = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: question }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }

      const data = await res.json();

      // Remove the loading line and add the answer
      setLines((prev) => {
        const filtered = prev.filter((l) =>
          typeof l === "string" || l.type !== "loading"
        );
        return [...filtered, { text: data.answer, type: "ai" }];
      });
    } catch (err) {
      setLines((prev) => {
        const filtered = prev.filter((l) =>
          typeof l === "string" || l.type !== "loading"
        );
        return [
          ...filtered,
          { text: `[agent error: ${err.message}]`, type: "error" },
        ];
      });
    } finally {
      setLoading(false);
    }
  }, []);

  const handleKey = (e) => {
    if (e.key !== "Enter" || !input.trim() || loading) return;
    const raw = input.trim();
    const cmd = raw.toLowerCase();
    setLines((prev) => [...prev, `harshit@os:~$ ${raw}`]);

    // Built-in commands
    const builtins = {
      help: "Commands: about, projects, experience, blog, contact, skills, theme, clear\n  Or just type a question to ask the AI agent.",
      skills: Object.entries(skills)
        .map(([k, v]) => `  ${k}: ${v.join(", ")}`)
        .join("\n"),
      clear: null,
    };

    if (builtins[cmd] !== undefined) {
      if (cmd === "clear") setLines([]);
      else setLines((prev) => [...prev, builtins[cmd]]);
    } else if (
      ["about", "projects", "experience", "blog", "contact"].includes(cmd)
    ) {
      onCommand(cmd);
      setLines((prev) => [...prev, `Opening ${cmd}...`]);
    } else if (cmd === "theme") {
      onCommand("__theme");
      setLines((prev) => [...prev, "Theme toggled."]);
    } else {
      // Everything else goes to the AI agent
      const question = cmd.startsWith("ask ")
        ? raw.slice(4).trim()
        : raw;
      askAgent(question);
    }
    setInput("");
  };

  // Render a single line (string or object)
  const renderLine = (l, i) => {
    // Simple string lines (boot, commands, etc.)
    if (typeof l === "string") {
      const line = l || "";
      let color = "#aaa";
      if (line.startsWith("[OK]")) color = t.terminal;
      else if (line.startsWith("harshit@")) color = "#00bfff";
      else if (line.startsWith("command not found")) color = "#ff6b6b";
      else if (line.startsWith("Commands:") || line.startsWith("  ")) color = "#ccc";
      return (
        <div key={i} style={{ color, whiteSpace: "pre-wrap" }}>
          {line || "\u00A0"}
        </div>
      );
    }

    // Typed line objects (AI response, loading, error)
    if (l.type === "loading") {
      return (
        <div key={i} style={{ color: t.accent, whiteSpace: "pre-wrap" }}>
          <LoadingDots text={l.text} />
        </div>
      );
    }
    if (l.type === "ai") {
      return (
        <div
          key={i}
          style={{
            color: t.terminal,
            whiteSpace: "pre-wrap",
            padding: "4px 0",
            borderLeft: `2px solid ${t.terminal}`,
            paddingLeft: 8,
            marginTop: 2,
            marginBottom: 2,
          }}
        >
          {l.text}
        </div>
      );
    }
    if (l.type === "error") {
      return (
        <div key={i} style={{ color: "#ff6b6b", whiteSpace: "pre-wrap" }}>
          {l.text}
        </div>
      );
    }
    return null;
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
      {lines.map(renderLine)}
      {bootDone && (
        <div style={{ display: "flex", alignItems: "center" }}>
          <span style={{ color: "#00bfff" }}>harshit@os:~$&nbsp;</span>
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            disabled={loading}
            placeholder={loading ? "waiting for agent..." : ""}
            style={{
              background: "transparent",
              border: "none",
              color: loading ? "#666" : "#e0e0e0",
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

// Animated dots for the loading indicator
function LoadingDots({ text }) {
  const [dots, setDots] = useState("");

  useEffect(() => {
    const iv = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 400);
    return () => clearInterval(iv);
  }, []);

  return <span>{text}{dots}</span>;
}
