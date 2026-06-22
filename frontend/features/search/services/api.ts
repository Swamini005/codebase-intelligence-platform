import { SearchResultChunk } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export async function searchRepositoryCode(
  repositoryId: number,
  query: string,
  limit: number = 5
): Promise<SearchResultChunk[]> {
  const params = new URLSearchParams({ query, limit: String(limit) });
  const res = await fetch(`${API_URL}/search/${repositoryId}?${params.toString()}`);
  if (!res.ok) throw new Error("Search query failed");
  return res.json();
}
