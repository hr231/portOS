import { useState, useEffect } from "react";

import { themes } from "./data/themes";
import { useIsMobile } from "./hooks/useIsMobile";

import RetroBtn from "./components/ui/RetroBtn";
import Window from "./components/ui/Window";
import DesktopIcon from "./components/ui/DesktopIcon";

import AboutContent from "./components/panels/AboutContent";
import ExperienceContent from "./components/panels/ExperienceContent";
import ProjectsContent from "./components/panels/ProjectsContent";
import BlogContent from "./components/panels/BlogContent";
import ContactContent from "./components/panels/ContactContent";
import TerminalContent from "./components/panels/TerminalContent";
import ResumeViewer from "./components/panels/ResumeViewer";

const desktopItems = [
  { id: "about", icon: "👤", label: "About Me" },
  { id: "experience", icon: "💼", label: "Experience" },
  { id: "projects", icon: "🗂️", label: "Projects" },
  { id: "blog", icon: "📝", label: "Blog" },
  { id: "contact", icon: "📡", label: "Contact" },
  { id: "terminal", icon: "⬛", label: "Terminal" },
  { id: "resume", icon: "📄", label: "Resume" },
];

export default function App() {
  const [mode, setMode] = useState("dark");
  const t = themes[mode];
  const isMobile = useIsMobile();
  const [openWins, setOpenWins] = useState([]);
  const [zOrder, setZOrder] = useState([]);
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const iv = setInterval(() => setTime(new Date()), 30000);
    return () => clearInterval(iv);
  }, []);

  const open = (id) => {
    if (id === "__theme") {
      setMode((m) => (m === "dark" ? "light" : "dark"));
      return;
    }
    if (!openWins.includes(id)) setOpenWins((p) => [...p, id]);
    focusWin(id);
  };

  const close = (id) => {
    setOpenWins((p) => p.filter((w) => w !== id));
    setZOrder((p) => p.filter((w) => w !== id));
  };

  const focusWin = (id) =>
    setZOrder((p) => [...p.filter((w) => w !== id), id]);

  const getZ = (id) => zOrder.indexOf(id) + 10;

  // Window definitions — maps id → { title, icon, content, pos }
  const wins = {
    about: {
      title: "About Me",
      icon: "👤",
      content: <AboutContent t={t} />,
      pos: { x: 100, y: 30 },
    },
    experience: {
      title: "Experience",
      icon: "💼",
      content: <ExperienceContent t={t} />,
      pos: { x: 140, y: 50 },
    },
    projects: {
      title: "Projects",
      icon: "🗂️",
      content: <ProjectsContent t={t} />,
      pos: { x: 180, y: 35 },
    },
    blog: {
      title: "Blog",
      icon: "📝",
      content: <BlogContent t={t} />,
      pos: { x: 130, y: 60 },
    },
    contact: {
      title: "Contact",
      icon: "📡",
      content: <ContactContent t={t} />,
      pos: { x: 200, y: 40 },
    },
    terminal: {
      title: "Terminal",
      icon: "⬛",
      content: <TerminalContent t={t} onCommand={open} />,
      pos: { x: 60, y: 50 },
    },
    resume: {
      title: "Resume.pdf — Document Viewer",
      icon: "📄",
      content: <ResumeViewer t={t} />,
      pos: { x: 160, y: 20 },
    },
  };

  // ─── MOBILE LAYOUT ─────────────────────────────────────
  if (isMobile) {
    const activeWin = zOrder.length ? zOrder[zOrder.length - 1] : null;

    return (
      <div
        style={{
          width: "100vw",
          height: "100vh",
          background: t.bg,
          display: "flex",
          flexDirection: "column",
          overflow: "hidden",
        }}
      >
        {/* Status bar */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            padding: "6px 12px",
            background: t.surfaceDark,
            borderBottom: `1px solid ${t.borderDark}`,
          }}
        >
          <span
            style={{
              fontFamily: "monospace",
              fontSize: 12,
              fontWeight: 700,
              color: t.titleBarText,
            }}
          >
            ◆ HarshitOS
          </span>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <span
              onClick={() => setMode((m) => (m === "dark" ? "light" : "dark"))}
              style={{ cursor: "pointer", fontSize: 16 }}
            >
              {mode === "dark" ? "☀️" : "🌙"}
            </span>
            <span style={{ fontFamily: "monospace", fontSize: 11, color: t.muted }}>
              {time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
            </span>
          </div>
        </div>

        {/* Content area */}
        <div style={{ flex: 1, overflow: "hidden", position: "relative" }}>
          {activeWin && wins[activeWin] ? (
            <Window
              title={wins[activeWin].title}
              onClose={() => close(activeWin)}
              t={t}
              isMobile={true}
              zIndex={20}
              onFocus={() => {}}
            >
              {wins[activeWin].content}
            </Window>
          ) : (
            <div
              style={{
                padding: 20,
                display: "grid",
                gridTemplateColumns: "repeat(3, 1fr)",
                gap: 8,
                justifyItems: "center",
                paddingTop: 30,
              }}
            >
              {desktopItems.map((d) => (
                <DesktopIcon
                  key={d.id}
                  icon={d.icon}
                  label={d.label}
                  t={t}
                  onClick={() => open(d.id)}
                />
              ))}
            </div>
          )}
        </div>

        {/* Bottom nav */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            padding: "6px 0",
            background: t.surfaceDark,
            borderTop: `1px solid ${t.borderDark}`,
          }}
        >
          {desktopItems.slice(0, 5).map((d) => (
            <div
              key={d.id}
              onClick={() => open(d.id)}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 2,
                cursor: "pointer",
                opacity: activeWin === d.id ? 1 : 0.6,
              }}
            >
              <span style={{ fontSize: 18 }}>{d.icon}</span>
              <span
                style={{
                  fontSize: 9,
                  color: t.titleBarText,
                  fontFamily: "monospace",
                }}
              >
                {d.label.split(" ")[0]}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  // ─── DESKTOP LAYOUT ────────────────────────────────────
  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: t.bg,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Scanline overlay (dark mode only) */}
      {mode === "dark" && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 300,
            pointerEvents: "none",
            background:
              "repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px)",
          }}
        />
      )}

      {/* Desktop icons grid */}
      <div
        style={{
          position: "absolute",
          top: 12,
          left: 12,
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 2,
          zIndex: 5,
        }}
      >
        {desktopItems.map((d) => (
          <DesktopIcon
            key={d.id}
            icon={d.icon}
            label={d.label}
            t={t}
            onClick={() => open(d.id)}
          />
        ))}
      </div>

      {/* Open windows */}
      {openWins.map((id) => {
        const w = wins[id];
        if (!w) return null;
        return (
          <Window
            key={id}
            title={w.title}
            initialPos={w.pos}
            zIndex={getZ(id)}
            onFocus={() => focusWin(id)}
            onClose={() => close(id)}
            t={t}
            isMobile={false}
          >
            {w.content}
          </Window>
        );
      })}

      {/* Taskbar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 36,
          background: t.surface,
          borderTop: `2px solid ${t.border}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 4px",
          zIndex: 400,
        }}
      >
        {/* Left side — Start button + open window tabs */}
        <div style={{ display: "flex", alignItems: "center", gap: 3 }}>
          <RetroBtn
            t={t}
            style={{ fontWeight: 700, padding: "4px 14px", marginRight: 4 }}
          >
            ◆ HarshitOS
          </RetroBtn>
          <div
            style={{
              width: 1,
              height: 24,
              background: t.borderDark,
              margin: "0 4px",
            }}
          />
          {openWins.map((id) => (
            <RetroBtn
              key={id}
              t={t}
              active={zOrder[zOrder.length - 1] === id}
              onClick={() => focusWin(id)}
              style={{ minWidth: 80, textAlign: "left", fontSize: 11 }}
            >
              {wins[id]?.icon} {wins[id]?.title}
            </RetroBtn>
          ))}
        </div>

        {/* System tray */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            padding: "2px 8px",
            borderLeft: `1px solid ${t.borderDark}`,
            borderTop: `1px solid ${t.borderDark}`,
            borderRight: `1px solid ${t.border}`,
            borderBottom: `1px solid ${t.border}`,
          }}
        >
          <span
            onClick={() => setMode((m) => (m === "dark" ? "light" : "dark"))}
            style={{ cursor: "pointer", fontSize: 14, userSelect: "none" }}
          >
            {mode === "dark" ? "☀️" : "🌙"}
          </span>
          <span
            style={{
              fontFamily: "'Segoe UI', Tahoma, sans-serif",
              fontSize: 11,
              color: t.text,
            }}
          >
            {time.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
          </span>
        </div>
      </div>
    </div>
  );
}
