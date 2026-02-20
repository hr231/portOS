/**
 * VoiceButton — push-to-talk / always-on mic button for the web UI.
 *
 * States:
 *   idle       → mic off, waiting for click
 *   listening  → mic on, capturing audio
 *   processing → audio sent, waiting for agent response
 *   speaking   → agent response playing via TTS
 *
 * Phase 2: Connect to WebSocket /api/voice or LiveKit JS SDK.
 */

import { useState } from "react";

export default function VoiceButton({ t, onStatusChange }) {
  const [status, setStatus] = useState("idle"); // idle | listening | processing | speaking

  const handleClick = () => {
    // TODO: Phase 2 — implement WebRTC/WebSocket voice connection
    if (status === "idle") {
      setStatus("listening");
      onStatusChange?.("listening");
      // Placeholder: auto-return to idle after 2s
      setTimeout(() => {
        setStatus("idle");
        onStatusChange?.("idle");
      }, 2000);
    } else {
      setStatus("idle");
      onStatusChange?.("idle");
    }
  };

  const icons = {
    idle: "🎙️",
    listening: "🔴",
    processing: "⏳",
    speaking: "🔊",
  };

  const labels = {
    idle: "Voice",
    listening: "Listening...",
    processing: "Thinking...",
    speaking: "Speaking...",
  };

  return (
    <button
      onClick={handleClick}
      title={labels[status]}
      style={{
        width: 36,
        height: 36,
        borderRadius: "50%",
        border: `2px solid ${status === "listening" ? "#ff4444" : t.border}`,
        background: status === "listening" ? "#ff444422" : t.surface,
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 16,
        transition: "all 0.2s",
        animation: status === "listening" ? "pulse 1.5s infinite" : "none",
      }}
    >
      {icons[status]}
    </button>
  );
}
