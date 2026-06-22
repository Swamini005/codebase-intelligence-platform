"use client";

import React, { use, useState, useEffect } from "react";
import { FolderGit2, RefreshCw, Layers, Cpu, Search, Key, Code } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { SearchBar } from "@/components/SearchBar";
import { ChatInterface } from "@/components/ChatInterface";
import { DependencyGraph } from "@/components/DependencyGraph";
import { ArchitectureView } from "@/components/ArchitectureView";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";

import { useChat } from "@/features/chat/hooks/useChat";
import { useSearch } from "@/features/search/hooks/useSearch";
import { useArchitecture } from "@/features/architecture/hooks/useArchitecture";
import { useAnalytics } from "@/features/analytics/hooks/useAnalytics";

interface PageProps {
  params: Promise<{ id: string }>;
}

export default function RepositoryDetail({ params }: PageProps) {
  const resolvedParams = use(params);
  const repoId = parseInt(resolvedParams.id, 10);

  const [repoName, setRepoName] = useState("Loading...");
  
  // Custom Feature hooks
  const { messages, isLoading: isChatLoading, sendMessage } = useChat(repoId);
  const { query, setQuery, results, isLoading: isSearchLoading, performSearch } = useSearch(repoId);
  const { graphData, archData, isLoading: isArchLoading } = useArchitecture(repoId);
  const { report, isLoading: isAnalyticsLoading } = useAnalytics(repoId);

  useEffect(() => {
    // Stub fetching repository metadata from local list
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    fetch(`${API_URL}/repositories/${repoId}`)
      .then((res) => res.json())
      .then((data) => setRepoName(data.name || "Repository"))
      .catch(() => setRepoName("Repository"));
  }, [repoId]);

  const handleReindex = async () => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    await fetch(`${API_URL}/repositories/${repoId}/reindex`, { method: "POST" });
    alert("Reindexing pipeline triggered!");
  };

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-800 pb-4">
        <div className="flex items-center gap-3">
          <FolderGit2 className="h-8 w-8 text-blue-400" />
          <div>
            <h2 className="text-xl font-bold text-zinc-150">{repoName}</h2>
            <p className="text-xs text-zinc-400 font-mono">Repo ID: {repoId}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleReindex}>
            <RefreshCw className="h-4 w-4 mr-1.5" /> Reindex Codebase
          </Button>
        </div>
      </div>

      <Tabs defaultValue="chat">
        <TabsList className="mb-4">
          <TabsTrigger value="chat">Codebase Chat</TabsTrigger>
          <TabsTrigger value="search">Semantic Search</TabsTrigger>
          <TabsTrigger value="architecture">Architecture Mapping</TabsTrigger>
          <TabsTrigger value="dependency">Dependency Graph</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        <TabsContent value="chat">
          <ChatInterface
            messages={messages}
            isLoading={isChatLoading}
            onSendMessage={sendMessage}
          />
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          <SearchBar
            value={query}
            onChange={setQuery}
            onSearch={performSearch}
            isLoading={isSearchLoading}
            placeholder="Search codebase semantically..."
          />
          
          <div className="space-y-4 mt-4">
            {results.length === 0 && !isSearchLoading && (
              <div className="text-zinc-500 text-sm italic">Type query and search.</div>
            )}
            {results.map((res, idx) => (
              <Card key={idx} className="border-zinc-800 bg-zinc-900/30">
                <CardHeader className="py-2.5 bg-zinc-900/50 border-b border-zinc-850 flex flex-row items-center justify-between">
                  <div className="text-xs font-mono text-blue-400 font-semibold flex items-center gap-1.5">
                    <Code className="h-3.5 w-3.5" />
                    {res.metadata.file_path} (Lines {res.metadata.start_line}-{res.metadata.end_line})
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
        </TabsContent>

        <TabsContent value="architecture">
          {isArchLoading ? (
            <div className="text-zinc-500 text-sm">Analyzing modules...</div>
          ) : (
            <ArchitectureView modules={archData?.modules || []} />
          )}
        </TabsContent>

        <TabsContent value="dependency">
          {isArchLoading ? (
            <div className="text-zinc-500 text-sm">Building call relations...</div>
          ) : (
            <DependencyGraph
              nodes={graphData?.nodes || []}
              edges={graphData?.edges || []}
            />
          )}
        </TabsContent>

        <TabsContent value="analytics">
          {isAnalyticsLoading ? (
            <div className="text-zinc-500 text-sm">Running complexity scans...</div>
          ) : (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader><CardTitle className="text-sm">Static Code Metrics</CardTitle></CardHeader>
                  <CardContent className="space-y-3">
                    {report?.metrics.map((m, idx) => (
                      <div key={idx} className="flex justify-between border-b border-zinc-800 pb-1.5 text-sm">
                        <span className="text-zinc-400">{m.name}</span>
                        <span className="font-semibold text-zinc-200">{m.value}{m.unit}</span>
                      </div>
                    ))}
                  </CardContent>
                </Card>
                
                <Card>
                  <CardHeader><CardTitle className="text-sm">Structure & Health Insights</CardTitle></CardHeader>
                  <CardContent className="space-y-2">
                    {report?.insights.map((insight, idx) => (
                      <div key={idx} className="text-xs text-zinc-300 bg-zinc-900 px-3 py-2 rounded-md border border-zinc-850">
                        {insight}
                      </div>
                    ))}
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
