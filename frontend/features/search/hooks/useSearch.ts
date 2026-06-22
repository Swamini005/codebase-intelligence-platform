"use client";

import { useState } from "react";
import { SearchResultChunk } from "../types";
import { searchRepositoryCode } from "../services/api";

export function useSearch(repositoryId: number) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResultChunk[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const performSearch = async (searchQuery: string = query) => {
    if (!searchQuery.trim()) return;
    try {
      setIsLoading(true);
      setError(null);
      const data = await searchRepositoryCode(repositoryId, searchQuery);
      setResults(data);
    } catch (err: any) {
      setError(err.message || "Semantic search failed");
    } finally {
      setIsLoading(false);
    }
  };

  return {
    query,
    setQuery,
    results,
    isLoading,
    error,
    performSearch,
  };
}
