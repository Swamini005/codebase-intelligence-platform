import { Repository, IndexStatus } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchRepositories(): Promise<Repository[]> {
  const res = await fetch(`${API_URL}/repositories`);
  if (!res.ok) throw new Error("Failed to fetch repositories");
  return res.json();
}

export async function fetchRepository(id: number): Promise<Repository> {
  const res = await fetch(`${API_URL}/repositories/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch repository ${id}`);
  return res.json();
}

export async function connectGithubRepo(githubUrl: string): Promise<Repository> {
  const res = await fetch(`${API_URL}/repositories/github`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ github_url: githubUrl }),
  });
  if (!res.ok) throw new Error("Failed to connect GitHub repository");
  return res.json();
}

export async function triggerRepositoryIndexing(id: number): Promise<IndexStatus> {
  const res = await fetch(`${API_URL}/repositories/${id}/index`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to trigger indexing");
  return res.json();
}

export async function fetchIndexStatus(id: number): Promise<IndexStatus> {
  const res = await fetch(`${API_URL}/repositories/${id}/status`);
  if (!res.ok) throw new Error("Failed to fetch index status");
  return res.json();
}
