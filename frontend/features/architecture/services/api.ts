import { DependencyGraphData, ArchitectureData } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function fetchDependencyGraph(repoId: number): Promise<DependencyGraphData> {
  const res = await fetch(`${API_URL}/repositories/${repoId}/dependencies`);
  if (!res.ok) throw new Error("Failed to fetch dependency graph data");
  return res.json();
}

export async function fetchArchitectureOverview(repoId: number): Promise<ArchitectureData> {
  const res = await fetch(`${API_URL}/repositories/${repoId}/architecture`);
  if (!res.ok) throw new Error("Failed to fetch architecture overview data");
  return res.json();
}
