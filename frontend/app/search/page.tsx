"use client";

import React, { useState } from "react";
import { Search, Code } from "lucide-react";
import { SearchBar } from "@/components/SearchBar";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface SearchResultChunk {
  document: string;
  metadata: {
    file_path: string;
    start_line: number;
    end_line: number;
    repository_id: number;
  };
  score?: number;
}

export default function GlobalSearch() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResultChunk[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleGlobalSearch = async () => {
    if (!query.trim()) return;
    try {
      setIsLoading(true);
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
      const res = await fetch(`${API_URL}/search?query=${encodeURIComponent(query)}`, {
        method: "POST"
      });
      if (!res.ok) throw new Error("Search failed");
      const data = await res.json();
      setResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="border-b border-zinc-800 pb-4">
        <h2 className="text-xl font-bold text-zinc-150">Global Code Search</h2>
        <p className="text-xs text-zinc-400">Search logic structure, variables, and comments across all indexations.</p>
      </div>

      <SearchBar
        value={query}
        onChange={setQuery}
        onSearch={handleGlobalSearch}
        isLoading={isLoading}
      />

      <div className="space-y-4">
        {results.length === 0 && !isLoading && (
          <div className="text-zinc-500 text-sm italic">Type query and search.</div>
        )}
        {results.map((res, idx) => (
          <Card key={idx} className="border-zinc-800 bg-zinc-900/30">
            <CardHeader className="py-2.5 bg-zinc-900/50 border-b border-zinc-850 flex flex-row items-center justify-between">
              <div className="text-xs font-mono text-blue-400 font-semibold flex items-center gap-1.5">
                <Code className="h-3.5 w-3.5" />
                Repo {res.metadata.repository_id}: {res.metadata.file_path} (Lines {res.metadata.start_line}-{res.metadata.end_line})
              </div>
              {res.score && (
                <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full font-mono">
                  Score: {res.score.toFixed(2)}
                </span>
              )}
            </CardHeader>
            <CardContent className="p-3 font-mono text-xs text-zinc-300 overflow-x-auto whitespace-pre">
              {res.document}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
