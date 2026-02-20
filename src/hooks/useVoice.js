/**
 * useVoice — React hook for browser voice interaction.
 *
 * Manages:
 *   - Microphone access (getUserMedia)
 *   - WebSocket connection to /api/voice
 *   - Audio playback of TTS responses
 *   - Connection state
 *
 * Phase 2: Implement with WebSocket or LiveKit JS SDK.
 *
 * Usage:
 *   const { status, startListening, stopListening, isSupported } = useVoice();
 */

import { useState, useRef, useCallback } from "react";
import { API_URL } from "../config";

export function useVoice() {
  const [status, setStatus] = useState("idle"); // idle | connecting | listening | processing | speaking
  const wsRef = useRef(null);
  const streamRef = useRef(null);

  const isSupported =
    typeof navigator !== "undefined" &&
    typeof navigator.mediaDevices !== "undefined" &&
    typeof navigator.mediaDevices.getUserMedia === "function";

  const startListening = useCallback(async () => {
    // TODO: Phase 2 — implement WebSocket voice connection
    // 1. Request mic access: navigator.mediaDevices.getUserMedia({ audio: true })
    // 2. Connect WebSocket: new WebSocket(API_URL.replace("http", "ws") + "/api/voice")
    // 3. Stream audio chunks to WebSocket
    // 4. Receive TTS audio from WebSocket and play via AudioContext
    setStatus("listening");
    console.log("[useVoice] Not yet implemented — Phase 2");
  }, []);

  const stopListening = useCallback(() => {
    // TODO: Phase 2 — close WebSocket, stop mic stream
    setStatus("idle");
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
  }, []);

  return {
    status,
    startListening,
    stopListening,
    isSupported,
  };
}
