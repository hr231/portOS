import { useState, useRef, useCallback, useEffect } from "react";

export function useDrag(initialPos, enabled) {
  const [pos, setPos] = useState(initialPos);
  const dragging = useRef(false);
  const offset = useRef({ x: 0, y: 0 });

  const onMouseDown = useCallback(
    (e) => {
      if (!enabled) return;
      dragging.current = true;
      offset.current = { x: e.clientX - pos.x, y: e.clientY - pos.y };
      e.preventDefault();
    },
    [pos, enabled]
  );

  useEffect(() => {
    const move = (e) => {
      if (dragging.current) {
        setPos({
          x: e.clientX - offset.current.x,
          y: e.clientY - offset.current.y,
        });
      }
    };
    const up = () => {
      dragging.current = false;
    };
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", up);
    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", up);
    };
  }, []);

  return { pos, onMouseDown };
}
