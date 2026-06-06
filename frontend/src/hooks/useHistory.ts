import { useState, useCallback } from "react";
import type { ScanResponse } from "../types";

const STORAGE_KEY = "litmus_history";
const MAX_HISTORY = 5;

export function useHistory() {
  const [history, setHistory] = useState<ScanResponse[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  const addScan = useCallback((scan: ScanResponse) => {
    setHistory((prev) => {
      const next = [scan, ...prev].slice(0, MAX_HISTORY);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      } catch {
        /* */
      }
      return next;
    });
  }, []);

  const clearHistory = useCallback(() => {
    setHistory([]);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  const getScan = useCallback(
    (scanId: string) => history.find((s) => s.scan_id === scanId) ?? null,
    [history]
  );

  return { history, addScan, clearHistory, getScan };
}
