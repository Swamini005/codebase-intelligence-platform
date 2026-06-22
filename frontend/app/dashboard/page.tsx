"use client";

import React, { useState } from "react";
import { FolderGit2, Plus, Terminal, RefreshCw, Layers, Cpu, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { RepositoryCard } from "@/components/RepositoryCard";
import { UploadRepositoryModal } from "@/components/UploadRepositoryModal";
import { useRepositories } from "@/features/repositories/hooks/useRepositories";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const router = useRouter();
  const { repositories, isLoading, error, refresh, addRepository } = useRepositories();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSelectRepository = (id: number) => {
    router.push(`/repository/${id}`);
  };

  const handleReindex = (id: number) => {
    console.log("Triggering reindex for ID:", id);
    // In full impl, this would post to /repositories/{id}/reindex
  };

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-lg bg-gradient-to-r from-blue-900/20 to-purple-900/20 border border-blue-900/30">
        <div className="space-y-1">
          <h2 className="text-xl font-bold text-zinc-150">Welcome to CodeIntel Platform</h2>
          <p className="text-sm text-zinc-400">Index repositories, search semantic logic, and chat with your codebase using RAG.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)} className="flex items-center gap-2">
          <Plus className="h-4 w-4" /> Add Repository
        </Button>
      </div>

      {/* System Overview Statistics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-4 rounded-lg bg-zinc-900/30 border border-zinc-850 flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-zinc-500 uppercase">Connected Repositories</div>
            <div className="text-2xl font-bold text-zinc-200 mt-1">{repositories.length}</div>
          </div>
          <FolderGit2 className="h-8 w-8 text-blue-500" />
        </div>
        <div className="p-4 rounded-lg bg-zinc-900/30 border border-zinc-850 flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-zinc-500 uppercase">Analysis Results</div>
            <div className="text-2xl font-bold text-zinc-200 mt-1">12</div>
          </div>
          <Layers className="h-8 w-8 text-emerald-500" />
        </div>
        <div className="p-4 rounded-lg bg-zinc-900/30 border border-zinc-850 flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-zinc-500 uppercase">Indexed Classes/Functions</div>
            <div className="text-2xl font-bold text-zinc-200 mt-1">452</div>
          </div>
          <Terminal className="h-8 w-8 text-purple-500" />
        </div>
        <div className="p-4 rounded-lg bg-zinc-900/30 border border-zinc-850 flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-zinc-500 uppercase">Embeddings Engine</div>
            <div className="text-xs font-mono font-bold text-zinc-400 mt-2">Gemini-Embedding</div>
          </div>
          <Cpu className="h-8 w-8 text-orange-500" />
        </div>
      </div>

      {/* Repositories listing */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-md font-bold text-zinc-350">Active Repositories</h3>
          <Button variant="outline" size="sm" onClick={refresh}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>

        {isLoading ? (
          <div className="text-zinc-500 text-sm italic">Loading repositories list...</div>
        ) : error ? (
          <div className="text-red-400 text-sm">Error: {error}</div>
        ) : repositories.length === 0 ? (
          <div className="text-zinc-500 text-sm italic py-8 border border-dashed border-zinc-800 rounded-lg text-center">
            No repositories connected yet. Click "Add Repository" to get started.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {repositories.map((repo) => (
              <RepositoryCard
                key={repo.id}
                id={repo.id}
                name={repo.name}
                githubUrl={repo.github_url}
                status={repo.status}
                onSelect={handleSelectRepository}
                onReindex={handleReindex}
              />
            ))}
          </div>
        )}
      </div>

      <UploadRepositoryModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConnectGithub={(url) => addRepository(url)}
        onUploadZip={(name) => console.log("Uploaded zip file metadata for:", name)}
      />
    </div>
  );
}
