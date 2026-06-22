export interface DependencyNode {
  id: string;
  label: string;
  type: string;
}

export interface DependencyEdge {
  source: string;
  target: string;
  type: string;
}

export interface DependencyGraphData {
  repository_id: number;
  nodes: DependencyNode[];
  edges: DependencyEdge[];
}

export interface ArchitectureModule {
  name: string;
  files: string[];
  dependencies: string[];
}

export interface ArchitectureData {
  repository_id: number;
  modules: ArchitectureModule[];
}
