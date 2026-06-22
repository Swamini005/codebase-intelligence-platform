export type RepositoryStatus = "PENDING" | "INDEXING" | "COMPLETED" | "FAILED";

export interface Repository {
  id: number;
  name: string;
  github_url?: string;
  status: RepositoryStatus;
  created_at: string;
  updated_at: string;
}

export interface IndexStatus {
  repository_id: number;
  status: RepositoryStatus;
}
