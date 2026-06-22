"use client";

import React, { useState } from "react";
import { FolderGit2, Plus, RefreshCw, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useRepositories } from "@/features/repositories/hooks/useRepositories";
import { UploadRepositoryModal } from "@/components/UploadRepositoryModal";
import { useRouter } from "next/navigation";

export default function Repositories() {
  const router = useRouter();
  const { repositories, isLoading, error, refresh, addRepository } = useRepositories();
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-zinc-800 pb-4">
        <div>
          <h2 className="text-xl font-bold text-zinc-150">Connected Repositories</h2>
          <p className="text-xs text-zinc-400">View and manage your connected directories and GitHub accounts.</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={refresh}>
            <RefreshCw className="h-4 w-4" />
          </Button>
          <Button onClick={() => setIsModalOpen(true)} size="sm">
            <Plus className="h-4 w-4 mr-1.5" /> Connect Repo
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="text-zinc-500 text-sm italic">Loading your codebases...</div>
      ) : error ? (
        <div className="text-red-400 text-sm">Error: {error}</div>
      ) : (
        <div className="border border-zinc-800 rounded-lg overflow-hidden bg-zinc-950/40">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-zinc-800 bg-zinc-900/30 text-zinc-400 text-xs font-semibold">
                <th className="p-4">Repository Name</th>
                <th className="p-4">GitHub Connection</th>
                <th className="p-4">Status</th>
                <th className="p-4">Created Date</th>
                <th className="p-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody>
              {repositories.map((repo) => (
                <tr key={repo.id} className="border-b border-zinc-850 hover:bg-zinc-900/20 text-sm">
                  <td className="p-4 font-semibold text-zinc-200 flex items-center gap-2">
                    <FolderGit2 className="h-4.5 w-4.5 text-blue-400" />
                    {repo.name}
                  </td>
                  <td className="p-4 text-zinc-400 font-mono text-xs">{repo.github_url || "Local Upload"}</td>
                  <td className="p-4">
                    <span className={`px-2 py-0.5 text-xs font-semibold rounded-full border ${
                      repo.status === "COMPLETED" ? "bg-green-500/10 text-green-400 border-green-500/20" : "bg-zinc-800 text-zinc-400"
                    }`}>
                      {repo.status}
                    </span>
                  </td>
                  <td className="p-4 text-zinc-400">{new Date(repo.created_at).toLocaleDateString()}</td>
                  <td className="p-4 text-right">
                    <Button variant="ghost" size="sm" onClick={() => router.push(`/repository/${repo.id}`)}>
                      Explore
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <UploadRepositoryModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onConnectGithub={(url) => addRepository(url)}
        onUploadZip={(name) => console.log("Upload zipped file metadata:", name)}
      />
    </div>
  );
}
