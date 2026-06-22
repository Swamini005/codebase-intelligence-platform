import React from "react";
import { Layers, Folder, PackageOpen } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";

interface Module {
  name: string;
  files: string[];
  dependencies: string[];
}

interface ArchitectureViewProps {
  modules: Module[];
}

export function ArchitectureView({ modules = [] }: ArchitectureViewProps) {
  return (
    <Card className="border-zinc-800 bg-zinc-950/40">
      <CardHeader className="border-b border-zinc-800 py-3">
        <CardTitle className="text-sm font-bold flex items-center gap-2">
          <Layers className="h-4 w-4 text-purple-400" />
          Logical Architecture Boundaries
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {modules.map((m, idx) => (
          <div key={idx} className="border border-zinc-800 rounded-md p-4 bg-zinc-900/30 flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <PackageOpen className="h-4.5 w-4.5 text-blue-400" />
                <h4 className="text-sm font-semibold text-zinc-200">{m.name}</h4>
              </div>
              <div className="space-y-1">
                <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider">Module Files</div>
                <div className="space-y-1">
                  {m.files.map((f, fIdx) => (
                    <div key={fIdx} className="text-xs font-mono text-zinc-400 bg-zinc-900 px-2 py-1 rounded truncate">
                      {f}
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-zinc-850">
              <div className="text-[10px] font-bold text-zinc-500 uppercase tracking-wider mb-1">Depends On</div>
              <div className="flex flex-wrap gap-1">
                {m.dependencies.length > 0 ? (
                  m.dependencies.map((d, dIdx) => (
                    <span key={dIdx} className="text-[10px] px-2 py-0.5 rounded bg-blue-950/30 text-blue-400 border border-blue-900/30">
                      {d}
                    </span>
                  ))
                ) : (
                  <span className="text-[10px] text-zinc-650 italic">None</span>
                )}
              </div>
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
