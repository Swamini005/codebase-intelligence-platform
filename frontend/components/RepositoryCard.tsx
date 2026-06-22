import React from "react";
import { FolderGit2, RefreshCw, Terminal, ExternalLink } from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Button } from "./ui/button";

interface RepositoryCardProps {
  id: number;
  name: string;
  githubUrl?: string;
  status: string;
  onSelect: (id: number) => void;
  onReindex: (id: number) => void;
}

export function RepositoryCard({ id, name, githubUrl, status, onSelect, onReindex }: RepositoryCardProps) {
  const getStatusColor = (currentStatus: string) => {
    switch (currentStatus) {
      case "COMPLETED":
        return "bg-green-500/20 text-green-400 border-green-500/30";
      case "INDEXING":
        return "bg-blue-500/20 text-blue-400 border-blue-500/30 animate-pulse";
      case "FAILED":
        return "bg-red-500/20 text-red-400 border-red-500/30";
      default:
        return "bg-zinc-800 text-zinc-400 border-zinc-700";
    }
  };

  return (
    <Card className="hover:border-zinc-700 transition-all duration-300">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-md font-bold flex items-center gap-2">
          <FolderGit2 className="h-5 w-5 text-blue-400" />
          {name}
        </CardTitle>
        <span className={`px-2 py-0.5 text-xs font-semibold rounded-full border ${getStatusColor(status)}`}>
          {status}
        </span>
      </CardHeader>
      <CardContent>
        {githubUrl && (
          <a
            href={githubUrl}
            target="_blank"
            rel="noreferrer"
            className="text-xs text-zinc-400 hover:text-zinc-200 flex items-center gap-1 mb-4"
          >
            <ExternalLink className="h-3.5 w-3.5" />
            {githubUrl}
          </a>
        )}
        <div className="flex gap-2 mt-2">
          <Button variant="default" size="sm" onClick={() => onSelect(id)}>
            Open Platform
          </Button>
          <Button variant="outline" size="sm" className="h-8 w-8 p-0" onClick={() => onReindex(id)}>
            <RefreshCw className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
