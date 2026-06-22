"use client";

import { useState, useEffect } from "react";
import { DependencyGraphData, ArchitectureData } from "../types";
import { fetchDependencyGraph, fetchArchitectureOverview } from "../services/api";

export function useArchitecture(repositoryId: number) {
  const [graphData, setGraphData] = useState<DependencyGraphData | null>(null);
  const [archData, setArchData] = useState<ArchitectureData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadArchitecture = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const [graph, arch] = await Promise.all([
          fetchDependencyGraph(repositoryId),
          fetchArchitectureOverview(repositoryId)
        ]);

        setGraphData(graph);
        setArchData(arch);
      } catch (err: any) {
        setError(err.message || "Failed to load architecture insights");
      } finally {
        setIsLoading(false);
      }
    };

    loadArchitecture();
  }, [repositoryId]);

  return {
    graphData,
    archData,
    isLoading,
    error,
  };
}
