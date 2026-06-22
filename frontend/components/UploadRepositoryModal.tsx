import React, { useState } from "react";
import { Dialog, DialogHeader, DialogTitle, DialogDescription } from "./ui/dialog";
import { Button } from "./ui/button";
import { Input } from "./ui/input";

interface UploadRepositoryModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConnectGithub: (url: string) => void;
  onUploadZip: (name: string, file: File) => void;
}

export function UploadRepositoryModal({ isOpen, onClose, onConnectGithub, onUploadZip }: UploadRepositoryModalProps) {
  const [activeTab, setActiveTab] = useState<"github" | "upload">("github");
  const [githubUrl, setGithubUrl] = useState("");
  const [repoName, setRepoName] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleSubmitGithub = (e: React.FormEvent) => {
    e.preventDefault();
    if (githubUrl.trim()) {
      onConnectGithub(githubUrl);
      setGithubUrl("");
      onClose();
    }
  };

  const handleSubmitUpload = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoName.trim() && selectedFile) {
      onUploadZip(repoName, selectedFile);
      setRepoName("");
      setSelectedFile(null);
      onClose();
    }
  };

  return (
    <Dialog isOpen={isOpen} onClose={onClose}>
      <DialogHeader>
        <DialogTitle>Add Repository</DialogTitle>
        <DialogDescription>
          Connect a GitHub repository or upload a local zipped codebase directory to start indexing.
        </DialogDescription>
      </DialogHeader>

      <div className="flex gap-2 border-b border-zinc-800 my-4 pb-2">
        <button
          onClick={() => setActiveTab("github")}
          className={`text-sm font-medium pb-1.5 px-1 border-b-2 transition-all ${
            activeTab === "github" ? "border-blue-500 text-zinc-150" : "border-transparent text-zinc-500 hover:text-zinc-300"
          }`}
        >
          GitHub Repository
        </button>
        <button
          onClick={() => setActiveTab("upload")}
          className={`text-sm font-medium pb-1.5 px-1 border-b-2 transition-all ${
            activeTab === "upload" ? "border-blue-500 text-zinc-150" : "border-transparent text-zinc-500 hover:text-zinc-300"
          }`}
        >
          Upload Zip File
        </button>
      </div>

      {activeTab === "github" ? (
        <form onSubmit={handleSubmitGithub} className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Repository GitHub URL</label>
            <Input
              placeholder="https://github.com/username/repository"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              required
            />
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="outline" type="button" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">Connect & Index</Button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleSubmitUpload} className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Repository Display Name</label>
            <Input
              placeholder="my-awesome-project"
              value={repoName}
              onChange={(e) => setRepoName(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="text-xs font-semibold text-zinc-400 mb-1.5 block">Zipped Codebase (.zip)</label>
            <input
              type="file"
              accept=".zip"
              className="flex w-full text-zinc-300 text-sm file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-zinc-800 file:text-zinc-200 file:text-sm file:font-semibold hover:file:bg-zinc-700"
              onChange={(e) => {
                if (e.target.files && e.target.files.length > 0) {
                  setSelectedFile(e.target.files[0]);
                }
              }}
              required
            />
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <Button variant="outline" type="button" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">Upload & Index</Button>
          </div>
        </form>
      )}
    </Dialog>
  );
}
