import React, { useState } from "react";
import { Network, FileCode2, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { Input } from "./ui/input";

interface Node {
  id: string;
  label: string;
  type: string;
}

interface Edge {
  source: string;
  target: string;
}

interface DependencyGraphProps {
  nodes: Node[];
  edges: Edge[];
}

export function DependencyGraph({ nodes = [], edges = [] }: DependencyGraphProps) {
  const [filter, setFilter] = useState("");

  const filteredNodes = nodes.filter(
    (n) => n.label.toLowerCase().includes(filter.toLowerCase()) || n.type.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <Card className="border-zinc-800 bg-zinc-950/40">
      <CardHeader className="border-b border-zinc-800 py-3 flex flex-row items-center justify-between">
        <CardTitle className="text-sm font-bold flex items-center gap-2">
          <Network className="h-4 w-4 text-emerald-400" />
          Code Dependency Analyzer
        </CardTitle>
        <Input
          placeholder="Filter modules..."
          className="w-48 h-8 text-xs bg-zinc-900 border-zinc-800"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </CardHeader>
      <CardContent className="p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Left Column: Modules List */}
        <div className="border border-zinc-800 rounded-md p-3 bg-zinc-900/30">
          <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">Detected Modules</h4>
          <div className="space-y-2">
            {filteredNodes.map((n) => (
              <div key={n.id} className="flex items-center gap-2 p-2 rounded bg-zinc-900 border border-zinc-800 hover:border-zinc-700">
                <FileCode2 className="h-4 w-4 text-blue-400" />
                <div>
                  <div className="text-xs font-semibold text-zinc-200">{n.label}</div>
                  <div className="text-[10px] text-zinc-500 font-mono">{n.type}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Connection Flow Diagrams */}
        <div className="md:col-span-2 border border-zinc-800 rounded-md p-3 bg-zinc-900/30 flex flex-col justify-between">
          <div>
            <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-2">Dependency Relations</h4>
            <div className="space-y-2">
              {edges.map((e, idx) => (
                <div key={idx} className="flex items-center gap-3 text-xs p-2 rounded bg-zinc-900/50 border border-zinc-850">
                  <span className="font-mono text-zinc-300">{e.source}</span>
                  <ArrowRight className="h-3.5 w-3.5 text-zinc-500" />
                  <span className="font-mono text-zinc-300">{e.target}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="mt-4 text-[10px] text-zinc-500 italic">
            * Interactive WebGL/D3 Graph view placeholder. Will load complete NetworkX callgraph on demand.
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
