"use client";

import { useState, useEffect } from "react";
import { AnalyticsReport } from "../types";
import { fetchRepositoryAnalytics } from "../services/api";

export function useAnalytics(repositoryId: number) {
  const [report, setReport] = useState<AnalyticsReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await fetchRepositoryAnalytics(repositoryId);
        setReport(data);
      } catch (err: any) {
        setError(err.message || "Failed to load repository analytics");
      } finally {
        setIsLoading(false);
      }
    };

    loadAnalytics();
  }, [repositoryId]);

  return {
    report,
    isLoading,
    error,
  };
}
