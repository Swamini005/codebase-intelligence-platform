export interface SearchChunkMetadata {
  file_path: string;
  start_line: number;
  end_line: number;
  repository_id: number;
}

export interface SearchResultChunk {
  document: string;
  metadata: SearchChunkMetadata;
  score?: number;
}
