"use client";

import React, { useState, useEffect } from "react";
import { Cpu } from "lucide-react";
import { ChatInterface } from "@/components/ChatInterface";
import { useChat } from "@/features/chat/hooks/useChat";

interface Repository {
  id: number;
  name: string;
}

export default function GlobalChat() {
  const [repositories, setRepositories] = useState<Repository[]>([]);
  const [selectedRepoId, setSelectedRepoId] = useState<number | null>(null);

  useEffect(() => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
    fetch(`${API_URL}/repositories`)
      .then((res) => res.json())
      .then((data) => {
        setRepositories(data);
        if (data.length > 0) {
          setSelectedRepoId(data[0].id);
        }
      })
      .catch((e) => console.error("Failed to load repositories", e));
  }, []);

  const currentRepoId = selectedRepoId || 0;
  // Initialize chat hook conditional on repo selection
  const { messages, isLoading, sendMessage } = useChat(currentRepoId);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-zinc-150">Global RAG Assistant</h2>
          <p className="text-xs text-zinc-400">Ask questions and generate documentation about the selected codebase.</p>
        </div>
        <div>
          {repositories.length > 0 ? (
            <div className="flex items-center gap-2">
              <label className="text-xs text-zinc-400 font-semibold uppercase">Target Codebase:</label>
              <select
                value={currentRepoId}
                onChange={(e) => setSelectedRepoId(parseInt(e.target.value, 10))}
                className="bg-zinc-900 border border-zinc-800 rounded px-2 py-1 text-xs text-zinc-200"
              >
                {repositories.map((repo) => (
                  <option key={repo.id} value={repo.id}>
                    {repo.name}
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <span className="text-xs text-zinc-550">No repository connected yet</span>
          )}
        </div>
      </div>

      {selectedRepoId ? (
        <ChatInterface
          messages={messages}
          isLoading={isLoading}
          onSendMessage={sendMessage}
        />
      ) : (
        <div className="h-[400px] flex flex-col items-center justify-center border border-dashed border-zinc-850 rounded-lg text-zinc-500">
          <Cpu className="h-8 w-8 text-zinc-700 mb-2 animate-pulse" />
          <span className="text-sm">Please connect a repository in the dashboard to start a conversation.</span>
        </div>
      )}
    </div>
  );
}
